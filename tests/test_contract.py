import copy,hashlib,json,re
from pathlib import Path
import pytest
from gltest.direct import create_address
ROOT=Path(__file__).parents[1]
SOURCE=json.loads((ROOT/'fixtures/source.json').read_bytes())
BODY=(ROOT/'fixtures/graph.json').read_bytes().decode('utf-8')
def deploy(vm,build):
 vm.warp('2026-10-21T00:00:00Z');c=build(str(ROOT/'contract.py'),sdk_version='v0.2.12')
 assert hasattr(c,'lock_source'),'lock_source API missing'
 return c
def serve(vm,body=BODY,status=200):vm.mock_web(re.escape(SOURCE['test_url']),{'status':status,'body':body})
def opened(vm,c,body=BODY):
 serve(vm,body);c.lock_source('demo',SOURCE['test_url'],hashlib.sha256(body.encode('utf-8')).hexdigest(),'["auth"]')
def test_exact_fixture_bytes_use_declared_digest(direct_vm,direct_deploy):
 c=deploy(direct_vm,direct_deploy);raw=(ROOT/'fixtures/graph.json').read_bytes();assert hashlib.sha256(raw).hexdigest()==SOURCE['sha256'];serve(direct_vm,raw.decode('utf-8'));c.lock_source('exact',SOURCE['test_url'],SOURCE['sha256'],'["auth"]')
 assert c.get_record('exact')['source_sha256']==SOURCE['sha256']
@pytest.mark.parametrize('url',[
 'https://raw.githubusercontent.com/a/b/main/profile08/projects/change-cascade/fixtures/graph.json',
 'https://raw.githubusercontent.com/a/b/'+'0'*40+'/profile08/projects/other/fixtures/graph.json',
 'https://raw.githubusercontent.com/a/b/'+'0'*40+'/x/../profile08/projects/change-cascade/fixtures/graph.json',
 'https://raw.githubusercontent.com/a/b/'+'0'*40+'/profile08/projects/change-cascade/fixtures/graph.json?raw=1'])
def test_commit_namespace_and_canonical_locator_boundaries(direct_vm,direct_deploy,url):
 c=deploy(direct_vm,direct_deploy)
 with direct_vm.expect_revert('commit-pinned'):c.lock_source('demo',url,'0'*64,'["auth"]')
@pytest.mark.parametrize('body',['x','[]','{}','{'+(' '*32768)+'}','\ufeff{}'],ids=['invalid','array','empty','oversize','bom'])
def test_source_schema_json_and_byte_bounds(direct_vm,direct_deploy,body):
 c=deploy(direct_vm,direct_deploy)
 with direct_vm.expect_revert():opened(direct_vm,c,body)
def test_source_failure_and_independent_packet_forgery(direct_vm,direct_deploy):
 c=deploy(direct_vm,direct_deploy);opened(direct_vm,c);c.derive('demo',0)
 assert direct_vm.run_validator() is True
 packet=copy.deepcopy(c.get_record('demo')['last_capture']);packet['binding']['record_id']='forged'
 assert direct_vm.run_validator(leader_result=packet) is False
 packet=copy.deepcopy(c.get_record('demo')['last_capture']);packet['result']={'forged':True}
 assert direct_vm.run_validator(leader_result=packet) is False
 direct_vm.clear_mocks();serve(direct_vm,BODY+' ');assert direct_vm.run_validator() is False
def test_owner_cas_and_terminal_revoke(direct_vm,direct_deploy):
 c=deploy(direct_vm,direct_deploy);opened(direct_vm,c);other=create_address('outsider')
 with direct_vm.prank(other):
  with direct_vm.expect_revert('owner only'):c.derive('demo',0)
  with direct_vm.expect_revert('owner only'):c.revoke('demo',0,'withdraw')
 with direct_vm.expect_revert('stale revision'):c.derive('demo',1)
 c.derive('demo',0);direct_vm.clear_mocks();c.revoke('demo',1,'Synthetic review withdrawn')
 assert c.get_record('demo')['status']=='REVOKED'
 with direct_vm.expect_revert():c.derive('demo',2)
 with direct_vm.expect_revert():c.revoke('demo',2,'again')
 with direct_vm.expect_revert('already used'):opened(direct_vm,c)

def test_canonical_scc_stages_and_downstream_impact(direct_vm,direct_deploy):
 c=deploy(direct_vm,direct_deploy);opened(direct_vm,c);r=c.derive('demo',0)
 assert r['groups']==[{'id':'api','members':['api','cache'],'cyclic':True},{'id':'archive','members':['archive','ingest'],'cyclic':True},{'id':'auth','members':['auth'],'cyclic':False},{'id':'dashboard','members':['dashboard'],'cyclic':False},{'id':'secrets','members':['secrets'],'cyclic':False},{'id':'theme','members':['theme'],'cyclic':False}]
 assert r['condensation_edges']==[{'prerequisite':'api','dependent':'dashboard'},{'prerequisite':'auth','dependent':'api'},{'prerequisite':'secrets','dependent':'auth'},{'prerequisite':'theme','dependent':'dashboard'}]
 assert r['stages']==[['archive','secrets','theme'],['auth'],['api'],['dashboard']]
 assert r['impact_groups']==['api','auth','dashboard'] and r['impact_nodes']==['api','auth','cache','dashboard'] and r['selected_nodes']==['auth'] and r['cyclic_group_count']==2
 assert c.preview_impact('demo','["cache"]')['impact_nodes']==['api','cache','dashboard']
 assert c.preview_impact('demo','["dashboard"]')['impact_nodes']==['dashboard']
 c.confirm('demo',1);assert c.get_record('demo')['status']=='CONFIRMED' and direct_vm.run_validator() is True

def test_self_loop_is_atomic_cycle_and_independent_nodes_share_stage(direct_vm,direct_deploy):
 c=deploy(direct_vm,direct_deploy);p={'schema':'ChangeCascade-graph-v1','nodes':[{'id':'b','label':'B'},{'id':'A','label':'A'}],'dependencies':[{'dependent':'A','prerequisite':'A'}]}
 body=json.dumps(p);serve(direct_vm,body);c.lock_source('demo',SOURCE['test_url'],hashlib.sha256(body.encode()).hexdigest(),'["A"]');r=c.derive('demo',0)
 assert r['groups']==[{'id':'A','members':['A'],'cyclic':True},{'id':'b','members':['b'],'cyclic':False}] and r['stages']==[['A','b']] and r['impact_nodes']==['A']

def test_empty_dependencies_and_selection_canonicalization(direct_vm,direct_deploy):
 c=deploy(direct_vm,direct_deploy);p={'schema':'ChangeCascade-graph-v1','nodes':[{'id':'z','label':'Z'},{'id':'auth','label':'Auth'}],'dependencies':[]};body=json.dumps(p);serve(direct_vm,body);c.lock_source('demo',SOURCE['test_url'],hashlib.sha256(body.encode()).hexdigest(),'["z","auth"]');r=c.derive('demo',0)
 assert r['stages']==[['auth','z']] and r['selected_nodes']==['auth','z'] and r['impact_nodes']==['auth','z']

@pytest.mark.parametrize('kind',['unknown','duplicateid','unknownendpoint','duplicateedge','edgefields','nodefields','badid','emptylabel','toomanynodes','toomanyedges','duplicatejson'])
def test_strict_dependency_graph_boundaries(direct_vm,direct_deploy,kind):
 p=json.loads(BODY)
 if kind=='unknown':p['extra']=0
 if kind=='duplicateid':p['nodes'][1]['id']=p['nodes'][0]['id']
 if kind=='unknownendpoint':p['dependencies'][0]['prerequisite']='missing'
 if kind=='duplicateedge':p['dependencies'].append(p['dependencies'][0])
 if kind=='edgefields':p['dependencies'][0]['extra']=1
 if kind=='nodefields':p['nodes'][0]['extra']=1
 if kind=='badid':p['nodes'][0]['id']='bad id'
 if kind=='emptylabel':p['nodes'][0]['label']=''
 if kind=='toomanynodes':p['nodes']=[{'id':'v'+str(i),'label':'Synthetic'} for i in range(13)]
 if kind=='toomanyedges':p['dependencies']=[p['dependencies'][0]]*41
 c=deploy(direct_vm,direct_deploy)
 body=json.dumps(p)
 if kind=='duplicatejson':body=BODY.replace('"schema":','"schema":"duplicate","schema":',1)
 with direct_vm.expect_revert():opened(direct_vm,c,body)

@pytest.mark.parametrize('selection',['[]','["missing"]','["auth","auth"]','{"auth":true}','[true]'])
def test_strict_selected_node_set(direct_vm,direct_deploy,selection):
 c=deploy(direct_vm,direct_deploy);serve(direct_vm)
 with direct_vm.expect_revert():c.lock_source('demo',SOURCE['test_url'],SOURCE['sha256'],selection)

def test_confirmation_fresh_source_failure_keeps_derived(direct_vm,direct_deploy):
 c=deploy(direct_vm,direct_deploy);opened(direct_vm,c);c.derive('demo',0);direct_vm.clear_mocks();serve(direct_vm,'gone',404)
 with direct_vm.expect_revert('SOURCE'):c.confirm('demo',1)
 assert c.get_record('demo')['status']=='DERIVED' and c.get_record('demo')['revision']==1
