"""DEP-MOUNT 2026 | PHASE 7M-5
ML-guided, failure-aware J3 adapter design screening.
One-cell Google Colab compatible. Requires previously generated real 7L-2 DOE CSV.
NO synthetic replacement if DOE missing. NO automatic hardware or CAD approval.
"""
from pathlib import Path
import io, zipfile
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.neighbors import NearestNeighbors

SEED = 2026
rng = np.random.default_rng(SEED)
OUT = Path('DEP_MOUNT_7M5_Evidence')
OUT.mkdir(exist_ok=True)
DOE = Path('DEP_MOUNT_7L2_Adapter_Joint_DOE.csv')
if not DOE.is_file():
    try:
        from google.colab import files
        print('Upload the actual DEP_MOUNT_7L2_Adapter_Joint_DOE.csv file from 7L-2.')
        uploaded = files.upload()
        if DOE.name not in uploaded: raise FileNotFoundError(DOE.name)
    except ImportError:
        raise FileNotFoundError(f'Actual 7L-2 DOE required: {DOE.resolve()}')

df = pd.read_csv(DOE)
XCOL = ['thickness_mm','outer_diameter_mm','inner_diameter_mm','preload_N']
YCOL = ['Adapter mass (g)','Relative flexural rigidity','Thread-screen coverage',
        'Clamp + depth coverage','Friction no-slip coverage']
necessary = XCOL + YCOL + ['Geometry/stiffness gate']
missing = [x for x in necessary if x not in df]
if missing: raise ValueError('The DOE is not the documented Phase 7L-2 input. Missing: '+str(missing))
if df[necessary].isna().any().any(): raise ValueError('Missing numeric DOE entries; inspect input.')
if len(df) < 100: raise ValueError('DOE unexpectedly small; check the source file.')
print('='*85)
print('DEP-MOUNT 2026 | 7M-5 | FAILURE-AWARE J3 ADAPTER DOWNSLECTION')
print('='*85)
print(f'Loaded REAL 7L-2 analytical DOE: {len(df)} designs, not new test or FEA measurements')

# ---- Explicit and editable *project screening* thresholds, NOT design allowables ----
THREAD_MIN = 0.95             # hypothetical uncertainty-scenario coverage threshold
CLAMP_MIN  = 0.95             # hypothetical uncertainty-scenario coverage threshold
RIGID_MIN  = 0.80             # uncalibrated analytic rigidity proxy threshold
LIGAMENT_MIN_MM = 10.0        # discretionary manufacturing-review trigger, NOT standard
WASHER_EDGE_MIN_MM = 4.0     # provisional outer flat-face margin
BACKWALL_MIN_MM = 4.0        # provisional blind-hole remaining thickness
BOLT_HOLE_MM = 6.6           # M6 nominal clearance-hole CAD trial
WASHER_OD_MM = 12.0          # illustrative ISO7089 M6 washer outside diameter
DOWEL_HOLE_MM = 4.0          # nominal design dimension (not fit specification)
MOTOR_PCD_MM = 120.0
PIN_LENGTH_MM = 14.0
MATING_BLIND_MM = 7.5         # pin seated fully into mating plate
CRADLE_FLANGE_MM = 8.0
BASE_MASS_G = 518.50          # earlier SOLIDWORKS CAD adapter mass (not measured)

# ---- Physical fit/geometry: 4 bolts cardinal, 2 dowels at +/- 45 deg ----
R = MOTOR_PCD_MM / 2
ro = df['outer_diameter_mm']/2
ri = df['inner_diameter_mm']/2
boltr = BOLT_HOLE_MM/2
pinr = DOWEL_HOLE_MM/2
# Radial hole-to-bore / hole-to-periphery ligament, ignores chamfers and tolerance.
df['min_bolt_ligament_mm'] = np.minimum(R-boltr-ri, ro-R-boltr)
df['min_pin_ligament_mm'] = np.minimum(R-pinr-ri, ro-R-pinr)
df['min_washer_outer_land_mm'] = ro-R-WASHER_OD_MM/2
df['blind_hole_backwall_mm'] = df['thickness_mm']-MATING_BLIND_MM
# NOTE: if fully seated in a 7.5 mm blind plate hole, 14 mm pin projects 6.5 mm into cradle.
PIN_PROJECTION_MM = PIN_LENGTH_MM-MATING_BLIND_MM

# ---- Explicit gate checks; legacy friction coverage purposely not an J3 shear gate ----
gate = {
 'LEGACY_GEOMETRY_PROXY': df['Geometry/stiffness gate']>=0.5,
 'PLATE_RIGIDITY_PROXY': df['Relative flexural rigidity']>=RIGID_MIN,
 'THREAD_PROXY_COVERAGE': df['Thread-screen coverage']>=THREAD_MIN,
 'CLAMP_DEPTH_PROXY_COVERAGE': df['Clamp + depth coverage']>=CLAMP_MIN,
 'BOLT_EDGE_GEOMETRY': df['min_bolt_ligament_mm']>=LIGAMENT_MIN_MM,
 'PIN_EDGE_GEOMETRY': df['min_pin_ligament_mm']>=LIGAMENT_MIN_MM,
 'WASHER_FACE_LAND': df['min_washer_outer_land_mm']>=WASHER_EDGE_MIN_MM,
 'BLIND_HOLE_BACKWALL': df['blind_hole_backwall_mm']>=BACKWALL_MIN_MM,
}
for name, mask in gate.items(): df['PASS_'+name] = mask
PASSCOL = ['PASS_'+k for k in gate]
df['PASS_CONDITIONAL_PROXY_GATES'] = df[PASSCOL].all(axis=1)
df['FAIL_MODES'] = ['; '.join(name for name in gate if not df.at[i,'PASS_'+name]) or 'NONE'
                    for i in df.index]
df['J3_ENGINEERING_STATUS'] = np.where(df['PASS_CONDITIONAL_PROXY_GATES'],
 'CONDITIONAL_PROXY_SCREEN_ONLY__HARDWARE_OPEN',
 'FAIL_PROJECT_SCREEN__NOT_A_RELEASE')
df['FRICTION_ONLY_95PCT'] = df['Friction no-slip coverage'] >= THREAD_MIN

print('\n1. GATE STATISTICS (NOT PROBABILITIES OF REAL HARDWARE SUCCESS)')
print(f"Conditional J3 proxy pass: {int(df['PASS_CONDITIONAL_PROXY_GATES'].sum())}/{len(df)}")
print(f"Original friction-only >=95%: {int(df['FRICTION_ONLY_95PCT'].sum())}/{len(df)}")
print('Each gate failure count (overlapping categories):')
for name in gate: print(f'  {name:27s} {(~df["PASS_"+name]).sum():4d}')

# ---- Actual DOE ranking: screen values come from underlying 7L-2 analytical model ----
valid = df.loc[df['PASS_CONDITIONAL_PROXY_GATES']].copy()
if valid.empty:
    print('\nNO conditional candidates. Consider revisiting project screening assumptions.')
    valid['PARETO_MASS_RIGIDITY'] = pd.Series(dtype=bool)
else:
    # Nondominated by both (mass <= and rigidity >=), at least one strict.
    masses = valid['Adapter mass (g)'].to_numpy()
    rigidity = valid['Relative flexural rigidity'].to_numpy()
    pareto=[]
    for k in range(len(valid)):
        dominated = np.any((masses<=masses[k]) & (rigidity>=rigidity[k])
                           & ((masses<masses[k]) | (rigidity>rigidity[k])))
        pareto.append(not dominated)
    valid['PARETO_MASS_RIGIDITY']=pareto
    valid['Mass_saving_vs_CAD_g'] = BASE_MASS_G-valid['Adapter mass (g)']
    valid['Rank_by_mass'] = valid['Adapter mass (g)'].rank(method='first').astype(int)
    valid = valid.sort_values(['Adapter mass (g)','Relative flexural rigidity'],ascending=[True,False])
    print('\n2. ACTUAL PHYSICS-DOE CANDIDATES: SORTED AFTER GATES')
    cols = XCOL+['Adapter mass (g)','Mass_saving_vs_CAD_g','Relative flexural rigidity',
           'Thread-screen coverage','Clamp + depth coverage','min_bolt_ligament_mm',
           'min_pin_ligament_mm','PARETO_MASS_RIGIDITY']
    print(valid[cols].head(10).round(4).to_string(index=True))
    print('All candidates remain conditional: no physical J3 pin/contact verification.')

# ---- ML: surrogate predicts old 7L-2 *model outputs*, not unseen J3 joint behavior ----
train_idx, test_idx = train_test_split(np.arange(len(df)), test_size=.25, random_state=42)
Xtrain, Xtest = df.iloc[train_idx][XCOL],df.iloc[test_idx][XCOL]
Ytrain, Ytest = df.iloc[train_idx][YCOL],df.iloc[test_idx][YCOL]
models={
 'Adapter mass (g)':make_pipeline(PolynomialFeatures(3,include_bias=False),
                                 StandardScaler(),Ridge(alpha=.01)),
 'Relative flexural rigidity':make_pipeline(PolynomialFeatures(3,include_bias=False),
                                 StandardScaler(),Ridge(alpha=.01)),
 'Thread-screen coverage':HistGradientBoostingRegressor(max_iter=180,learning_rate=.06,
                                 max_leaf_nodes=15,random_state=42),
 'Clamp + depth coverage':HistGradientBoostingRegressor(max_iter=180,learning_rate=.06,
                                 max_leaf_nodes=15,random_state=42),
 'Friction no-slip coverage':HistGradientBoostingRegressor(max_iter=180,learning_rate=.06,
                                 max_leaf_nodes=15,random_state=42)
}
metrics=[]; residuals={}; predictions={}
for col,model in models.items():
    model.fit(Xtrain,Ytrain[col])
    p=model.predict(Xtest)
    predictions[col]=p
    err=p-Ytest[col].to_numpy()
    residuals[col]=err
    item={'Response':col,'Heldout_R2':r2_score(Ytest[col],p),
          'Heldout_MAE':mean_absolute_error(Ytest[col],p),
          'Abs_error_95pct':np.quantile(abs(err),.95)}
    if col in ['Thread-screen coverage','Clamp + depth coverage']:
        actual=Ytest[col].to_numpy()>=.95
        estimated=p>=.95
        item['False_pass_count']=int(np.sum(estimated & (~actual)))
        item['False_reject_count']=int(np.sum((~estimated) & actual))
    metrics.append(item)
perf=pd.DataFrame(metrics)
print('\n3. HELD-OUT MODEL PERFORMANCE AND WRONG ENGINEERING GATE DECISIONS')
print(perf.round(5).to_string(index=False))

# ---- Surrogate proposes *unseen* configurations. They are not direct-physics verified. ----
NSEARCH=25000
lower=df[XCOL].min().to_numpy(); upper=df[XCOL].max().to_numpy()
Xvirtual=rng.uniform(lower,upper,size=(NSEARCH,len(XCOL)))
v=pd.DataFrame(Xvirtual,columns=XCOL)
for col,model in models.items(): v['ML_'+col]=model.predict(v[XCOL])
v['ML_mass_g']=v['ML_Adapter mass (g)']
v['ML_rigid']=v['ML_Relative flexural rigidity']
v['ML_thread']=v['ML_Thread-screen coverage']
v['ML_clamp']=v['ML_Clamp + depth coverage']
v['ML_friction_diagnostic']=v['ML_Friction no-slip coverage']
vr=v['outer_diameter_mm']/2; vi=v['inner_diameter_mm']/2
v['minimum_bolt_ligament_mm']=np.minimum(R-boltr-vi,vr-R-boltr)
v['minimum_pin_ligament_mm']=np.minimum(R-pinr-vi,vr-R-pinr)
v['washer_land_mm']=vr-R-WASHER_OD_MM/2
v['blind_backwall_mm']=v['thickness_mm']-MATING_BLIND_MM
# Prediction error allowance based on 95th percentile of HELD-OUT absolute errors.
# Heuristic guard band; not a statistical confidence interval.
err95={m['Response']:m['Abs_error_95pct'] for m in metrics}
v['risk_mass_g']=v['ML_mass_g']+err95['Adapter mass (g)']
v['risk_rigid']=v['ML_rigid']-err95['Relative flexural rigidity']
v['risk_thread']=v['ML_thread']-err95['Thread-screen coverage']
v['risk_clamp']=v['ML_clamp']-err95['Clamp + depth coverage']
# Distance from real training design points in normalized 4D feature space.
scale=(upper-lower);scalextr=(Xtrain.to_numpy()-lower)/scale
nn=NearestNeighbors(n_neighbors=1).fit(scalextr)
v['nearest_training_distance']=nn.kneighbors((Xvirtual-lower)/scale,return_distance=True)[0][:,0]
geom=(v['minimum_bolt_ligament_mm']>=LIGAMENT_MIN_MM)&(v['minimum_pin_ligament_mm']>=LIGAMENT_MIN_MM)&(v['washer_land_mm']>=WASHER_EDGE_MIN_MM)&(v['blind_backwall_mm']>=BACKWALL_MIN_MM)
predscreen=geom & (v['risk_rigid']>=RIGID_MIN)&(v['risk_thread']>=THREAD_MIN)&(v['risk_clamp']>=CLAMP_MIN)&(v['nearest_training_distance']<=.20)
virtual=v.loc[predscreen].sort_values('risk_mass_g').head(10).copy()
virtual['VERIFICATION']='ML_NOMINATED_ONLY__7L2_DIRECT_PHYSICS_AND_J3_CAD_NOT_DONE'
print('\n4. ML-SUGGESTED NEW CONFIGURATIONS (SURROGATE ONLY, NOT PASS/VERIFIED)')
print(f'{int(predscreen.sum())} / {NSEARCH} meet heuristic guard-banded surrogate screens.')
if len(virtual):
    print(virtual[XCOL+['ML_mass_g','risk_rigid','risk_thread','risk_clamp',
                      'nearest_training_distance','VERIFICATION']].head(5).round(4).to_string(index=False))
else: print('None meet the stringent surrogate screen. Stay with DOE shortlist.')

# ---- Independent J3 S1 pin statics: same for all adapter DOE designs ----
# The old 7L2 DOE has no contact/pin-bending training outputs. Accordingly
# these checks CANNOT be an ML-dependent ranking variable here.
F=np.array([-413.996,118.990,-118.990])
M_P=1000*np.array([24.226,28.999,44.0])
P=np.array([200.,0.,0.]); angle=np.deg2rad(45)
radial=np.array([np.cos(angle),np.sin(angle)])
tangent=np.array([-np.sin(angle),np.cos(angle)])
S1=[]
for interface,x,pcd in [('Motor',100.,120.),('Airframe',0.,150.)]:
    moment=M_P+np.cross(P-np.array([x,0.,0.]),F)
    transverse=-F[1:]
    torque=-moment[0]
    radius_mm=pcd/2
    base_1=transverse/2 + torque/(2*radius_mm)*tangent
    base_2=transverse/2 - torque/(2*radius_mm)*tangent
    pnom=max(np.linalg.norm(base_1),np.linalg.norm(base_2))
    force_sum=base_1+base_2
    assert np.allclose(force_sum,transverse)
    # Sweep arbitrary self-equilibrating radial force q, preserving Fx/Fy/Mx balance.
    samples=[]
    for q in np.linspace(-pnom,pnom,201):
        p1=np.linalg.norm(base_1+q*radial)
        p2=np.linalg.norm(base_2-q*radial)
        samples.append(max(p1,p2))
    p_worst=max(samples)
    A=np.pi*(DOWEL_HOLE_MM**2)/4
    for category,pforce in [('Nominal',pnom),('Radial_load_redistribution_sweep',p_worst)]:
        for e in [0.5,1.,2.,3.]:
            shear=pforce/A
            bend=32*pforce*e/(np.pi*DOWEL_HOLE_MM**3)
            vm=np.sqrt(bend**2+3*shear**2)
            S1.append({'Interface':interface,'Loading':category,'Lever_arm_assumption_mm':e,
                'Peak_pin_N':pforce,'Nominal_shear_MPa':shear,'Bending_stress_proxy_MPa':bend,
                'Combined_stress_proxy_MPa':vm,
                'Cradle_bearing_at_6mm_MPa':pforce/(DOWEL_HOLE_MM*6.),
                'Mating_bearing_at_6mm_MPa':pforce/(DOWEL_HOLE_MM*6.)})
s1=pd.DataFrame(S1)
print('\n5. J3 LOAD-PATH LIMITATION (DOES NOT DISTINGUISH ADAPTER THICKNESS/DIAMETERS)')
print(s1.loc[(s1['Lever_arm_assumption_mm']==3.)][['Interface','Loading','Peak_pin_N','Combined_stress_proxy_MPa']].round(2).to_string(index=False))
print('No valid pin strength or bearing allowable is available; these are demands, not PASS margins.')
print(f'14 mm nominal pin, seated {MATING_BLIND_MM:g} mm in mating plate -> {PIN_PROJECTION_MM:g} mm in cradle (before tolerance/chamfer).')

# ---- Why candidates fail, what design control might help ----
actions={
 'LEGACY_GEOMETRY_PROXY':'Review original 7L-2 proxy assumptions and geometric conflict.',
 'PLATE_RIGIDITY_PROXY':'Increase thickness or revise section; assess mass cost.',
 'THREAD_PROXY_COVERAGE':'Reduce preload or increase verified thread capacity/engagement.',
 'CLAMP_DEPTH_PROXY_COVERAGE':'Inspect clamp stack and engagement depth; avoid blind-hole bottoming.',
 'BOLT_EDGE_GEOMETRY':'Increase OD or reduce ID, or relocate bolt pattern ONLY if interfaces allow.',
 'PIN_EDGE_GEOMETRY':'Increase OD or reduce ID; preserve 120 mm dowel PCD.',
 'WASHER_FACE_LAND':'Increase OD or specify validated seating detail.',
 'BLIND_HOLE_BACKWALL':'Increase thickness or decrease blind depth after fit review.'
}
fail_rows=[]
for name in gate:
    fail_rows.append({'Failure_mode':name,'Count':int((~df['PASS_'+name]).sum()),'Potential_action':actions[name],
                      'Is_qualified_hardware_failure':'NO; project proxy or CAD-only check'})
failure=pd.DataFrame(fail_rows)
print('\n6. FAILURE-TO-CORRECTIVE-ACTION TABLE')
print(failure.to_string(index=False))

# ---- Engineering-focused figures ----
plt.rcParams.update({'figure.dpi':110,'savefig.dpi':190,'font.size':10})
def saveplot(name):
    plt.tight_layout();plt.savefig(OUT/name,bbox_inches='tight');plt.show();plt.close()

fig,ax=plt.subplots(figsize=(9,5))
ax.barh(failure['Failure_mode'],failure['Count']);ax.set_xlabel('DOE configurations failing this gate')
ax.set_title('Failure-mode audit — multiple flags can apply to one design');ax.grid(axis='x',alpha=.2)
saveplot('01_failure_modes.png')

fig,ax=plt.subplots(figsize=(9,6))
rejected=df.loc[~df['PASS_CONDITIONAL_PROXY_GATES']]
ax.scatter(rejected['Adapter mass (g)'],rejected['Relative flexural rigidity'],alpha=.25,s=13,label='Fails >=1 proxy gate')
if len(valid):
    ax.scatter(valid['Adapter mass (g)'],valid['Relative flexural rigidity'],alpha=.65,s=20,label='Conditional proxy screen')
    front=valid[valid['PARETO_MASS_RIGIDITY']].sort_values('Adapter mass (g)')
    ax.plot(front['Adapter mass (g)'],front['Relative flexural rigidity'],marker='o',label='Conditional mass–rigidity Pareto')
ax.axhline(RIGID_MIN,linestyle='--',linewidth=1,label='Project rigidity floor')
ax.axvline(BASE_MASS_G,linestyle=':',linewidth=1,label='Baseline CAD adapter mass')
ax.set_xlabel('Existing 7L-2 physics-model adapter mass (g)')
ax.set_ylabel('Analytical relative rigidity INDEX')
ax.set_title('Mass versus rigidity: conditional J3 candidates; joint not qualified');ax.legend(fontsize=8)
ax.grid(alpha=.2)
saveplot('02_mass_rigidity_failure_pareto.png')

fig,ax=plt.subplots(figsize=(8,5))
ax.scatter(Ytest['Thread-screen coverage'],predictions['Thread-screen coverage'],s=18,alpha=.5)
ax.plot([0,1],[0,1],ls='--',label='Ideal prediction')
ax.axvline(THREAD_MIN,ls=':');ax.axhline(THREAD_MIN,ls=':')
ax.set_xlim(0,1.02);ax.set_ylim(0,1.02);ax.set_xlabel('Actual held-out 7L-2 physics-model coverage')
ax.set_ylabel('ML prediction');ax.set_title('Near-threshold ML mistakes: false passes matter')
ax.grid(alpha=.2);ax.legend()
saveplot('03_thread_gate_false_pass_diagnostic.png')

fig,ax=plt.subplots(figsize=(9,5))
for interface in ['Motor','Airframe']:
    s=s1[(s1['Interface']==interface)&(s1['Loading']=='Radial_load_redistribution_sweep')]
    ax.plot(s['Lever_arm_assumption_mm'],s['Combined_stress_proxy_MPa'],marker='o',label=interface)
ax.set_title('J3 pin bending sensitivity: hypothetical peak radial redistribution')
ax.set_xlabel('Effective bending lever arm assumption (mm)')
ax.set_ylabel('Combined pin stress proxy (MPa)')
ax.grid(alpha=.2);ax.legend()
saveplot('04_J3_pin_bending_unverified.png')

if len(valid):
    best=valid.head(6).copy()
    fig,ax=plt.subplots(figsize=(9,4.8))
    ax.bar(np.arange(len(best)),best['Adapter mass (g)'])
    ax.axhline(BASE_MASS_G,linestyle='--',label='Current CAD mass 518.5 g')
    ax.set_xticks(np.arange(len(best)))
    ax.set_xticklabels([f'DOE-{i}' for i in best.index],rotation=0)
    ax.set_ylabel('Mass proxy (g)')
    ax.set_title('Top six actual DOE conditional configurations (NOT released)')
    ax.legend();ax.grid(axis='y',alpha=.2)
    saveplot('05_conditional_shortlist_mass.png')

# ---- Traceable files and configuration status ----
df.to_csv(OUT/'7M5_all_800_classified_designs.csv',index_label='DOE_source_row')
valid.head(20).to_csv(OUT/'7M5_top20_existing_DOE_conditional.csv',index_label='DOE_source_row')
virtual.to_csv(OUT/'7M5_unverified_ML_virtual_proposals.csv',index=False)
perf.to_csv(OUT/'7M5_heldout_ML_validation.csv',index=False)
# Row-level traceability: identify which held-out configurations ML misclassifies.
audit=df.iloc[test_idx][XCOL+['Thread-screen coverage','Clamp + depth coverage']].copy()
audit['DOE_source_row']=test_idx
audit['ML_pred_thread']=predictions['Thread-screen coverage']
audit['ML_pred_clamp']=predictions['Clamp + depth coverage']
audit['thread_false_pass']=(audit['ML_pred_thread']>=THREAD_MIN)&(audit['Thread-screen coverage']<THREAD_MIN)
audit['thread_false_reject']=(audit['ML_pred_thread']<THREAD_MIN)&(audit['Thread-screen coverage']>=THREAD_MIN)
audit['clamp_false_pass']=(audit['ML_pred_clamp']>=CLAMP_MIN)&(audit['Clamp + depth coverage']<CLAMP_MIN)
audit['clamp_false_reject']=(audit['ML_pred_clamp']<CLAMP_MIN)&(audit['Clamp + depth coverage']>=CLAMP_MIN)
audit.to_csv(OUT/'7M5_heldout_false_pass_audit.csv',index=False)
s1.to_csv(OUT/'7M5_S1_dowel_contact_sensitivity.csv',index=False)
failure.to_csv(OUT/'7M5_failure_to_corrective_action.csv',index=False)
summary=pd.DataFrame([
 {'Rule':'7L-2 original friction-only joint >=95% coverage','Value':str(int(df['FRICTION_ONLY_95PCT'].sum()))+' / '+str(len(df)), 'Interpretation':'No friction-only candidate passed assumed screen.'},
 {'Rule':'7M-5 conditional J3 geometric/legacy proxies','Value':str(len(valid))+' / '+str(len(df)),'Interpretation':'Not physical joint qualification.'},
 {'Rule':'Dowel projection if fully seated in 7.5 mm blind mating hole','Value':str(PIN_PROJECTION_MM)+' mm','Interpretation':'Nominal geometry only; tolerance/fit open.'},
 {'Rule':'FEA J3 vs B04 stress','Value':'38.86 vs 39.22 MPa','Interpretation':'Cradle geometry only, not pinned/contact joint model.'},
 {'Rule':'Actual bolt/dowel contact/fit/fatigue','Value':'OPEN','Interpretation':'Blocks engineering hardware release.'},
 {'Rule':'Unseen virtual ML proposals','Value':str(len(virtual)),'Interpretation':'Cannot be called physics rechecked.'}])
summary.to_csv(OUT/'7M5_decision_log.csv',index=False)
import hashlib
source_sha256=hashlib.sha256(DOE.read_bytes()).hexdigest()
(OUT/'READ_ME_FIRST.txt').write_text('DEP-MOUNT 2026 Phase 7M-5.\n'+
 'Input source SHA-256: '+source_sha256+'\n'+
 'This is an ML-guided screening of 800 original 7L-2 ANALYTICAL DOE cases.\n'+
 'The J3 dowel calculations are separate static demand proxies; cannot establish contact, fatigue,\n'+
 'thread stripping, retention, bolt preload or real reliability.\n'+
 'Existing DOE gate passes are conditional; virtual ML proposals have NO independent physics recheck.\n'+
 'No CAD release, hardware qualification, or flight design allowables.\n')
zipname='DEP_MOUNT_7M5_Evidence.zip'
with zipfile.ZipFile(zipname,'w',zipfile.ZIP_DEFLATED) as z:
    for f in OUT.iterdir():
        if f.is_file(): z.write(f,arcname=f.name)
print('\n7. FINAL DESIGN DECISION')
if len(valid):
    one=valid.iloc[0]
    print(f"Lightest conditional DOE: row {valid.index[0]}; mass={one['Adapter mass (g)']:.2f} g; "+
          f"rigidity index={one['Relative flexural rigidity']:.3f}, thread coverage={one['Thread-screen coverage']:.3f}.")
print('RETAIN existing J3 CAD as reference. Conditional DOE variants need fit+physics+CAD recheck.')
print('Do not describe the friction-only joint as robust or any J3 option as flight qualified.')
print('All J3 dowel strength, contact, retention, real preload/separation, fatigue and vibration: OPEN.')
print('CAD CHANGE: NOT AUTHORIZED | ENGINEERING RELEASE: HOLD')
print('Saved:',zipname,'with',len(list(OUT.iterdir())),'outputs')
try:
    from google.colab import files
    files.download(zipname)
except ImportError:
    pass