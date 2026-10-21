export const ascii=(a:string,b:string)=>a<b?-1:a>b?1:0;
function fields(value:any,keys:string[]):void{if(!value||typeof value!=='object'||Array.isArray(value)||Object.keys(value).sort(ascii).join('|')!==[...keys].sort(ascii).join('|'))throw Error('Unexpected schema fields.');}
const identifier=(s:unknown):s is string=>typeof s==='string'&&/^[A-Za-z][A-Za-z0-9_]{0,23}$/.test(s);
const integer=(v:unknown,min:number,max:number)=>typeof v==='number'&&Number.isInteger(v)&&v>=min&&v<=max;
const canonical=(v:any):string=>v&&typeof v==='object'?(Array.isArray(v)?'['+v.map(canonical).join(',')+']':'{'+Object.keys(v).sort(ascii).map(k=>JSON.stringify(k)+':'+canonical(v[k])).join(',')+'}'):JSON.stringify(v);

export type Graph={schema:string;nodes:{id:string;label:string}[];dependencies:{dependent:string;prerequisite:string}[]};
export type Cascade={groups:{id:string;members:string[];cyclic:boolean}[];node_group:Record<string,string>;condensation_edges:{prerequisite:string;dependent:string}[];stages:string[][];selected_nodes:string[];impact_groups:string[];impact_nodes:string[];cyclic_group_count:number};
// Match Python str.strip boundary whitespace; JS trim additionally removes BOM.
const pythonBoundaryWhitespace=/^[\u0009-\u000D\u001C-\u0020\u0085\u00A0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]|[\u0009-\u000D\u001C-\u0020\u0085\u00A0\u1680\u2000-\u200A\u2028\u2029\u202F\u205F\u3000]$/u;
export function validateGraph(value:unknown):Graph{
 const g=value as Graph;fields(g,['schema','nodes','dependencies']);if(g.schema!=='ChangeCascade-graph-v1'||!Array.isArray(g.nodes)||g.nodes.length<1||g.nodes.length>12||!Array.isArray(g.dependencies)||g.dependencies.length>40)throw Error('Graph schema or bounds.');
 const ids=new Set<string>();for(const n of g.nodes){fields(n,['id','label']);if(!identifier(n.id)||ids.has(n.id)||typeof n.label!=='string'||!n.label.length||Array.from(n.label).length>64||pythonBoundaryWhitespace.test(n.label))throw Error('Invalid node or duplicate ID.');ids.add(n.id);}
 const edges=new Set<string>();for(const e of g.dependencies){fields(e,['dependent','prerequisite']);if(!ids.has(e.dependent)||!ids.has(e.prerequisite))throw Error('Unknown dependency endpoint.');const key=e.dependent+'|'+e.prerequisite;if(edges.has(key))throw Error('Duplicate dependency.');edges.add(key);}
 return {schema:g.schema,nodes:g.nodes.map(n=>({...n})).sort((a,b)=>ascii(a.id,b.id)),dependencies:g.dependencies.map(e=>({...e})).sort((a,b)=>ascii(a.dependent,b.dependent)||ascii(a.prerequisite,b.prerequisite))};
}
export function selection(g:Graph,input:unknown):string[]{if(!Array.isArray(input)||input.length<1||input.length>12||input.some(x=>typeof x!=='string'||!g.nodes.some(n=>n.id===x))||new Set(input).size!==input.length)throw Error('Choose 1..12 distinct known nodes.');return [...input].sort(ascii);}
export function derive(g:Graph,input:string[]):Cascade{
 const selected=selection(g,input),ids=g.nodes.map(n=>n.id),n=ids.length,index=new Map(ids.map((id,i)=>[id,i]));
 // Independent bounded transitive closure, rather than the contract's two-pass DFS.
 const reach=ids.map((_,i)=>ids.map((_,j)=>i===j));for(const e of g.dependencies)reach[index.get(e.prerequisite)!][index.get(e.dependent)!]=true;
 for(let k=0;k<n;k++)for(let i=0;i<n;i++)for(let j=0;j<n;j++)reach[i][j]=reach[i][j]||(reach[i][k]&&reach[k][j]);
 const seen=new Set<string>(),groups:Cascade['groups']=[],node_group:Record<string,string>={};
 for(let i=0;i<n;i++){if(seen.has(ids[i]))continue;const members=ids.filter((_,j)=>reach[i][j]&&reach[j][i]).sort(ascii),id=members[0];for(const m of members){seen.add(m);node_group[m]=id;}groups.push({id,members,cyclic:members.length>1||g.dependencies.some(e=>e.dependent===id&&e.prerequisite===id)});}
 groups.sort((a,b)=>ascii(a.id,b.id));const edgeKeys=new Set(g.dependencies.map(e=>[node_group[e.prerequisite],node_group[e.dependent]]).filter(([a,b])=>a!==b).map(([a,b])=>a+'|'+b));
 const condensation_edges=[...edgeKeys].map(key=>{const [prerequisite,dependent]=key.split('|');return {prerequisite,dependent};}).sort((a,b)=>ascii(a.prerequisite,b.prerequisite)||ascii(a.dependent,b.dependent));
 const remaining=new Set(groups.map(g=>g.id)),stages:string[][]=[];while(remaining.size){const available=[...remaining].filter(id=>!condensation_edges.some(e=>e.dependent===id&&remaining.has(e.prerequisite))).sort(ascii);if(!available.length)throw Error('Condensation DAG invariant.');stages.push(available);available.forEach(id=>remaining.delete(id));}
 const impact_nodes=ids.filter((_,j)=>selected.some(s=>reach[index.get(s)!][j])).sort(ascii),impact_groups=[...new Set(impact_nodes.map(id=>node_group[id]))].sort(ascii);
 return {groups,node_group,condensation_edges,stages,selected_nodes:selected,impact_groups,impact_nodes,cyclic_group_count:groups.filter(g=>g.cyclic).length};
}
export function assertChainResult(g:Graph,selected:string[],r:unknown):void{if(canonical(derive(g,selected))!==canonical(r))throw Error('Chain cascade is inconsistent with its frozen graph/selection.');}
export function canConfirm(r:any,account:string):boolean{return !!account&&r?.owner?.toLowerCase()===account.toLowerCase()&&r?.status==='DERIVED'&&Array.isArray(r?.result?.groups);}
