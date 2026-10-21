# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import hashlib
import json
import re
from datetime import datetime, timezone


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise gl.vm.UserError('[EXPECTED] '+message)


def _canonical(value) -> str:
    return json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)


def _now() -> int:
    value=datetime.fromisoformat(gl.message_raw['datetime'].replace('Z','+00:00'))
    if value.tzinfo is None:
        value=value.replace(tzinfo=timezone.utc)
    delta=value.astimezone(timezone.utc)-datetime(1970,1,1,tzinfo=timezone.utc)
    return delta.days*86400+delta.seconds


def _identifier(value) -> None:
    _require(isinstance(value,str) and re.fullmatch(r'[A-Za-z][A-Za-z0-9_]{0,23}',value) is not None,'invalid ASCII identifier')


def _source_locator(url: str,digest: str) -> None:
    pattern=r'https://raw\.githubusercontent\.com/[A-Za-z0-9-]{1,39}/[A-Za-z0-9_.-]{1,100}/[0-9a-f]{40}/([A-Za-z0-9_.~/-]+)'
    match=re.fullmatch(pattern,url) if isinstance(url,str) and len(url)<=512 else None
    _require(match is not None and all(part not in ('','.','..') for part in url.split('/')[3:]) and url.endswith('/profile08/projects/change-cascade/fixtures/graph.json'),'commit-pinned project source required')
    _require(isinstance(digest,str) and re.fullmatch(r'[0-9a-f]{64}',digest) is not None,'invalid SHA256')


def _unique_pairs(pairs: list) -> dict:
    result={}
    for key,value in pairs:
        _require(key not in result,'duplicate JSON key')
        result[key]=value
    return result


def _parse_json(body: bytes):
    _require(1<=len(body)<=32768,'source byte bound')
    try:
        return json.loads(body.decode('utf-8'),object_pairs_hook=_unique_pairs)
    except (ValueError,UnicodeError,RecursionError):
        raise gl.vm.UserError('[SOURCE] invalid UTF-8 JSON')


def _fetch(url: str,digest: str) -> dict:
    response=gl.nondet.web.get(url,headers={'Accept':'application/json'})
    if response.status!=200 or response.body is None or not 1<=len(response.body)<=32768:
        raise gl.vm.UserError('[SOURCE] source unavailable or oversized')
    if hashlib.sha256(response.body).hexdigest()!=digest:
        raise gl.vm.UserError('[SOURCE] source byte SHA256 mismatch')
    return _validate(_parse_json(response.body))


def _validate(value) -> dict:
    _require(isinstance(value,dict) and set(value)=={'schema','nodes','dependencies'} and value['schema']=='ChangeCascade-graph-v1','graph schema fields')
    nodes=value['nodes'];edges=value['dependencies']
    _require(isinstance(nodes,list) and 1<=len(nodes)<=12,'node count 1..12')
    _require(isinstance(edges,list) and len(edges)<=40,'dependency count 0..40')
    ids=set()
    for node in nodes:
        _require(isinstance(node,dict) and set(node)=={'id','label'},'node fields')
        _identifier(node['id']);_require(node['id'] not in ids,'duplicate node ID');ids.add(node['id'])
        _require(isinstance(node['label'],str) and 1<=len(node['label'])<=64 and node['label']==node['label'].strip(),'node label bound')
    seen=set()
    for edge in edges:
        _require(isinstance(edge,dict) and set(edge)=={'dependent','prerequisite'},'dependency fields')
        _require(isinstance(edge['dependent'],str) and isinstance(edge['prerequisite'],str) and edge['dependent'] in ids and edge['prerequisite'] in ids,'unknown dependency endpoint')
        key=(edge['dependent'],edge['prerequisite']);_require(key not in seen,'duplicate dependency');seen.add(key)
    return {'schema':value['schema'],'nodes':sorted(nodes,key=lambda n:n['id']),'dependencies':sorted(edges,key=lambda e:(e['dependent'],e['prerequisite']))}


def _selection(text: str) -> list:
    _require(isinstance(text,str) and len(text)<=4096,'selected node JSON bound')
    values=_parse_json(text.encode('utf-8'))
    _require(isinstance(values,list) and 1<=len(values)<=12,'selection count 1..12')
    for value in values:
        _identifier(value)
    _require(len(set(values))==len(values),'duplicate selected node')
    return sorted(values)


def _known_selection(graph: dict,selection: list) -> None:
    names=set(n['id'] for n in graph['nodes'])
    _require(all(name in names for name in selection),'unknown selected node')


def _derive(graph: dict,selection: list) -> dict:
    _known_selection(graph,selection)
    names=[node['id'] for node in graph['nodes']]
    forward={name:[] for name in names};reverse={name:[] for name in names}
    for edge in graph['dependencies']:
        forward[edge['prerequisite']].append(edge['dependent']);reverse[edge['dependent']].append(edge['prerequisite'])
    for name in names:
        forward[name].sort();reverse[name].sort()
    visited=set();finish=[]
    def visit(node: str) -> None:
        if node in visited:
            return
        visited.add(node)
        for nxt in forward[node]:
            visit(nxt)
        finish.append(node)
    for name in names:
        visit(name)
    visited=set();components=[]
    def collect(node: str,members: list) -> None:
        if node in visited:
            return
        visited.add(node);members.append(node)
        for nxt in reverse[node]:
            collect(nxt,members)
    for node in reversed(finish):
        if node not in visited:
            members=[];collect(node,members);components.append(sorted(members))
    components.sort(key=lambda members:tuple(members))
    self_loops=set(e['dependent'] for e in graph['dependencies'] if e['dependent']==e['prerequisite'])
    groups=[{'id':members[0],'members':members,'cyclic':len(members)>1 or members[0] in self_loops} for members in components]
    membership={member:group['id'] for group in groups for member in group['members']}
    condensed=sorted(set((membership[e['prerequisite']],membership[e['dependent']]) for e in graph['dependencies'] if membership[e['prerequisite']]!=membership[e['dependent']]))
    successors={group['id']:[] for group in groups};indegree={group['id']:0 for group in groups}
    for prerequisite,dependent in condensed:
        successors[prerequisite].append(dependent);indegree[dependent]+=1
    remaining=set(indegree);stages=[]
    while remaining:
        available=sorted(group for group in remaining if indegree[group]==0)
        _require(bool(available),'condensation DAG invariant');stages.append(available)
        for group in available:
            remaining.remove(group)
            for dependent in successors[group]:
                indegree[dependent]-=1
    impacted=set(membership[node] for node in selection);pending=sorted(impacted)
    while pending:
        current=pending.pop(0)
        for dependent in successors[current]:
            if dependent not in impacted:
                impacted.add(dependent);pending.append(dependent)
    return {'groups':groups,'node_group':membership,'condensation_edges':[{'prerequisite':a,'dependent':b} for a,b in condensed],'stages':stages,'selected_nodes':selection,'impact_groups':sorted(impacted),'impact_nodes':sorted(node for node in names if membership[node] in impacted),'cyclic_group_count':sum(1 for group in groups if group['cyclic'])}


def _capture(url: str,digest: str,binding: dict) -> dict:
    def leader() -> dict:
        source=_fetch(url,digest);_known_selection(source,binding['selected_nodes'])
        return {'binding':binding,'source_sha256':digest,'source':source,'result':None if binding['operation']=='lock' else _derive(source,binding['selected_nodes'])}
    def validator(proposed: gl.vm.Result) -> bool:
        if not isinstance(proposed,gl.vm.Return):
            return False
        try:
            return _canonical(leader())==_canonical(proposed.calldata)
        except Exception:
            return False
    return gl.vm.run_nondet_unsafe(leader,validator)


class ChangeCascade(gl.Contract):
    records: TreeMap[str,str]

    def __init__(self):
        pass

    def _record(self,record_id: str) -> dict:
        _require(record_id in self.records,'unknown record')
        return json.loads(self.records[record_id])

    def _owner_revision(self,record: dict,expected_revision: int) -> None:
        _require(gl.message.sender_address.as_hex.lower()==record['owner'],'owner only')
        _require(type(expected_revision) is int and expected_revision==record['revision'],'stale revision')

    def _binding(self,record: dict,operation: str) -> dict:
        return {'protocol':'ChangeCascade-v1','chain_id':int(gl.message.chain_id),'contract':gl.message.contract_address.as_hex.lower(),'record_id':record['record_id'],'owner':record['owner'],'source_url':record['source_url'],'source_sha256':record['source_sha256'],'selected_nodes':record['selected_nodes'],'revision':record['revision'],'operation':operation,'observed_at':_now()}

    @gl.public.write
    def lock_source(self,record_id: str,source_url: str,source_sha256: str,seeds_json: str) -> None:
        _identifier(record_id);_source_locator(source_url,source_sha256);selected=_selection(seeds_json)
        _require(record_id not in self.records,'record ID already used')
        record={'record_id':record_id,'owner':gl.message.sender_address.as_hex.lower(),'source_url':source_url,'source_sha256':source_sha256,'selected_nodes':selected,'status':'LOCKED','revision':0,'locked_at':_now(),'derived_at':0,'confirmed_at':0,'revoked_at':0,'reason':'','certificate_id':'','result':None}
        packet=_capture(source_url,source_sha256,self._binding(record,'lock'));record['source']=packet['source'];record['last_capture']=packet
        self.records[record_id]=_canonical(record)

    @gl.public.write
    def derive(self,record_id: str,expected_revision: int) -> dict:
        record=self._record(record_id);self._owner_revision(record,expected_revision);_require(record['status']=='LOCKED','record not locked')
        packet=_capture(record['source_url'],record['source_sha256'],self._binding(record,'derive'));_require(_canonical(packet['source'])==_canonical(record['source']),'source snapshot mismatch')
        record['result']=packet['result'];record['last_capture']=packet;record['status']='DERIVED';record['revision']=1;record['derived_at']=_now();self.records[record_id]=_canonical(record)
        return record['result']

    @gl.public.write
    def confirm(self,record_id: str,expected_revision: int) -> None:
        record=self._record(record_id);self._owner_revision(record,expected_revision);_require(record['status']=='DERIVED','record not derived')
        packet=_capture(record['source_url'],record['source_sha256'],self._binding(record,'confirm'));_require(_canonical(packet['source'])==_canonical(record['source']) and _canonical(packet['result'])==_canonical(record['result']),'derived snapshot mismatch')
        record['status']='CONFIRMED';record['revision']=2;record['confirmed_at']=_now();record['last_capture']=packet;record['certificate_id']=hashlib.sha256(_canonical(packet).encode('utf-8')).hexdigest();self.records[record_id]=_canonical(record)

    @gl.public.write
    def revoke(self,record_id: str,expected_revision: int,reason: str) -> None:
        record=self._record(record_id);self._owner_revision(record,expected_revision);_require(record['status']!='REVOKED','record already revoked')
        _require(isinstance(reason,str) and 1<=len(reason)<=200 and reason==reason.strip(),'reason bound')
        record['status']='REVOKED';record['revision']+=1;record['reason']=reason;record['revoked_at']=_now();self.records[record_id]=_canonical(record)

    @gl.public.view
    def get_record(self,record_id: str) -> dict:
        return self._record(record_id)

    @gl.public.view
    def preview_impact(self,record_id: str,seeds_json: str) -> dict:
        record=self._record(record_id);result=_derive(record['source'],_selection(seeds_json))
        return {'selected_nodes':result['selected_nodes'],'impact_groups':result['impact_groups'],'impact_nodes':result['impact_nodes']}

    @gl.public.view
    def get_configuration(self) -> dict:
        return {'protocol':'ChangeCascade-v1','max_nodes':12,'max_dependencies':40,'max_source_bytes':32768,'real_changes_executed':False}
