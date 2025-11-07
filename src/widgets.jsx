import React, { useEffect, useState } from 'react';
import { createRoot } from 'react-dom/client';

function Stars({ value=0 }){
  const full = Math.round(value*2)/2;
  return (
    <div style={{display:'inline-flex', gap:6}} aria-label={`Рейтинг ${full} из 5`}>
      {[1,2,3,4,5].map(i=>{
        const filled = i <= Math.floor(full);
        const half = !filled && (i-0.5) <= full;
        return <span key={i} style={{fontSize:18, color: filled || half ? '#1FD3A3' : '#3b3b3b'}}>{half?'⯪':'★'}</span>
      })}
    </div>
  )
}

function ReviewsWidget(){
  const [items, setItems] = useState([]);
  const [avg, setAvg] = useState(0);
  const [loading, setLoading] = useState(true);
  const [name, setName] = useState('');
  const [text, setText] = useState('');
  const [rating, setRating] = useState(5);
  const [ok, setOk] = useState('');

  async function load(){
    setLoading(true);
    try{
      const r = await fetch('/reviews', { headers: {'accept':'application/json'}});
      if (r.ok){
        const j = await r.json();
        setItems(j.items||[]); setAvg(j.avg||0);
      }
    }catch(e){} finally { setLoading(false) }
  }
  useEffect(()=>{ load() }, [])

  async function submit(e){
    e.preventDefault();
    const body = { name: name.trim()||'Гость', text: text.trim(), rating: Number(rating)||5 };
    try{
      const r = await fetch('/reviews', { method:'POST', headers:{'content-type':'application/json'}, body: JSON.stringify(body)});
      if (r.ok){ setOk('Спасибо! Отзыв отправлен.'); setName(''); setText(''); setRating(5); load() }
      else setOk('Не удалось отправить. Попробуйте позже.');
    }catch(e){ setOk('Сеть недоступна. Попробуйте позже.') }
    setTimeout(()=>setOk(''), 4000);
  }

  return (
    <div style={{background:'#0c0f10', border:'1px solid #1f1f1f', borderRadius:12, padding:16, color:'#eaeaea'}}>
      <div style={{display:'flex', alignItems:'center', justifyContent:'space-between', marginBottom:12}}>
        <strong>Отзывы</strong>
        <div><Stars value={avg}/><span style={{marginLeft:8, opacity:.8}}>{avg.toFixed(1)}</span></div>
      </div>
      {loading ? <div>Загрузка…</div> :
        <div style={{display:'grid', gap:10}}>
          {(items||[]).slice(0,5).map((it,idx)=>(
            <div key={idx} style={{border:'1px solid #222', borderRadius:10, padding:10}}>
              <div style={{display:'flex', justifyContent:'space-between'}}>
                <strong>{it.name||'Гость'}</strong>
                <Stars value={it.rating||5}/>
              </div>
              <div style={{opacity:.9, marginTop:6, whiteSpace:'pre-wrap'}}>{it.text}</div>
            </div>
          ))}
        </div>
      }
      <form onSubmit={submit} style={{marginTop:14, display:'grid', gap:8}}>
        <input placeholder="Ваше имя" value={name} onChange={e=>setName(e.target.value)} style={{padding:'10px 12px', borderRadius:8, border:'1px solid #2a2a2a', background:'#0b0b0b', color:'#eaeaea'}}/>
        <textarea required placeholder="Отзыв" value={text} onChange={e=>setText(e.target.value)} rows={3} style={{padding:'10px 12px', borderRadius:8, border:'1px solid #2a2a2a', background:'#0b0b0b', color:'#eaeaea'}}/>
        <label style={{display:'flex', alignItems:'center', gap:8}}>Оценка:
          <select value={rating} onChange={e=>setRating(e.target.value)} style={{padding:'8px 10px', borderRadius:8, border:'1px solid #2a2a2a', background:'#0b0b0b', color:'#eaeaea'}}>
            {[5,4,3,2,1].map(v=><option key={v} value={v}>{v}</option>)}
          </select>
        </label>
        <button type="submit" style={{padding:'10px 14px', borderRadius:10, border:'1px solid #25d09a', background:'transparent', color:'#25d09a', cursor:'pointer'}}>Оставить отзыв</button>
        {ok && <div style={{marginTop:6, color:'#25d09a'}}>{ok}</div>}
      </form>
    </div>
  )
}

function LiveWidget(){
  const [visits, setVisits] = useState([]);
  async function load(){
    try{
      const r = await fetch('/live'); const j = await r.json(); setVisits(Array.isArray(j)?j:[]);
    }catch(e){}
  }
  useEffect(()=>{ load(); const id=setInterval(load, 10000); return ()=>clearInterval(id)}, []);
  return (
    <div style={{background:'#0c0f10', border:'1px solid #1f1f1f', borderRadius:12, padding:16, color:'#eaeaea'}}>
      <div style={{display:'flex', alignItems:'center', justifyContent:'space-between'}}>
        <strong>Live</strong><span style={{opacity:.8}}>{visits.length}</span>
      </div>
      <div style={{marginTop:10, display:'grid', gap:8}}>
        {visits.map((v, i)=>(
          <div key={i} style={{border:'1px solid #222', borderRadius:10, padding:10}}>
            <div><strong>{v.country||'—'}</strong> • {v.referrerTypeName||'Direct'}</div>
            <div style={{opacity:.8, fontSize:12}}>{(v.actionDetails?.[0]?.pageTitle)||v.lastActionDateTime||''}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

function mount(name, comp){
  document.querySelectorAll(`[data-widget="${name}"]`).forEach(n=> createRoot(n).render(comp));
}

mount('reviews', <ReviewsWidget/>);
mount('live', <LiveWidget/>);
