import { useState, useRef, useEffect } from 'react'

// ── Colors cho từng professor ─────────────────────────────────────────────────
const PROF_COLORS = ['#4fc3f7', '#81c784', '#ffb74d', '#f48fb1', '#ce93d8']
const ROLE_ICONS = {
  Empiricist: '📊', Theorist: '📐', Skeptic: '🔍',
  Pragmatist: '🔧', Historian: '📚',
}
const STATUS_STYLE = {
  VERIFIED:   { color: '#66bb6a', symbol: '✓' },
  UNVERIFIED: { color: '#ffa726', symbol: '?' },
  CONTESTED:  { color: '#ef5350', symbol: '✗' },
  OPINION:    { color: '#9e9e9e', symbol: '◈' },
}

// ── Components ────────────────────────────────────────────────────────────────

function SetupForm({ onStart, loading }) {
  const [field, setField] = useState('Distributed / Efficient LLM')
  const [topic, setTopic] = useState(
    'Tensor Parallelism vs Pipeline Parallelism vs MoE: đâu là chiến lược tối ưu để scale LLM lên hàng nghìn tỷ tham số?'
  )
  return (
    <div style={styles.setupWrap}>
      <h1 style={styles.logo}>⚔ Academic Debate Arena</h1>
      <p style={styles.subtitle}>Học qua tranh luận giữa các giáo sư AI hàng đầu</p>
      <div style={styles.form}>
        <label style={styles.label}>Lĩnh vực nghiên cứu</label>
        <input style={styles.input} value={field}
          onChange={e => setField(e.target.value)} />

        <label style={styles.label}>Câu hỏi tranh luận</label>
        <textarea style={{...styles.input, height: 90, resize: 'vertical'}}
          value={topic} onChange={e => setTopic(e.target.value)} />

        <button style={{...styles.btn, opacity: loading ? 0.6 : 1}}
          onClick={() => onStart(topic, field)} disabled={loading}>
          {loading ? 'Đang khởi động...' : '🚀 Bắt đầu tranh luận'}
        </button>
      </div>
    </div>
  )
}

function ProfessorCard({ prof, color }) {
  return (
    <div style={{...styles.profCard, borderColor: color + '55'}}>
      <div style={{...styles.profAvatar, background: color + '22', color}}>
        {ROLE_ICONS[prof.role] || '👤'}
      </div>
      <div>
        <div style={{...styles.profName, color}}>{prof.name}</div>
        <div style={styles.profUni}>{prof.university}</div>
        <div style={styles.profRole}>{prof.role}</div>
        <div style={styles.profStance}>{prof.stance}</div>
      </div>
    </div>
  )
}

function FactTag({ tag }) {
  const s = STATUS_STYLE[tag.status] || STATUS_STYLE.OPINION
  return (
    <div style={styles.factRow}>
      <span style={{...styles.factBadge, color: s.color, borderColor: s.color + '44'}}>
        {s.symbol} {tag.status}
      </span>
      <span style={styles.factClaim}>{tag.claim}</span>
      {tag.reason && <span style={styles.factReason}> — {tag.reason}</span>}
      {tag.sources?.map((src, i) => (
        <div key={i} style={styles.factSource}>↳ {src}</div>
      ))}
    </div>
  )
}

function TurnBubble({ turn, professors }) {
  const profIdx = professors.findIndex(p => p.key === turn.key)
  const color = PROF_COLORS[profIdx] || '#aaa'

  if (turn.type === 'moderator') {
    return (
      <div style={styles.modBubble}>
        <div style={styles.modLabel}>🎯 {turn.label}</div>
        <div style={styles.modContent}>{turn.content}</div>
      </div>
    )
  }

  if (turn.type === 'round') {
    return (
      <div style={styles.roundDivider}>── Round {turn.round} ──</div>
    )
  }

  return (
    <div style={{...styles.turnWrap, borderLeftColor: color}}>
      <div style={styles.turnHeader}>
        <span style={{...styles.turnName, color}}>{turn.name}</span>
        <span style={styles.turnRole}>{turn.role}</span>
        <span style={styles.turnNum}>Turn {turn.turn}</span>
      </div>
      <div style={styles.turnContent}>
        {turn.content}
        {turn.streaming && <span style={styles.cursor}>▍</span>}
      </div>
      {turn.fact_tags?.length > 0 && (
        <div style={styles.factWrap}>
          {turn.fact_tags.map((t, i) => <FactTag key={i} tag={t} />)}
        </div>
      )}
    </div>
  )
}

function FinalSummary({ content }) {
  const lines = content.split('\n')
  return (
    <div style={styles.finalWrap}>
      <div style={styles.finalTitle}>🏁 Key Insights</div>
      {lines.map((line, i) => (
        <div key={i} style={
          line.startsWith('**') ? styles.finalSection :
          line.startsWith('-') ? styles.finalBullet :
          styles.finalLine
        }>
          {line.replace(/\*\*/g, '')}
        </div>
      ))}
    </div>
  )
}

// ── Main App ──────────────────────────────────────────────────────────────────

export default function App() {
  const [phase, setPhase] = useState('setup') // setup | running | done
  const [status, setStatus] = useState('')
  const [professors, setProfessors] = useState([])
  const [turns, setTurns] = useState([])
  const [finalContent, setFinalContent] = useState('')
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [turns, status])

  const startDebate = (topic, field) => {
    setPhase('running')
    setStatus('Đang kết nối...')
    setTurns([])
    setProfessors([])
    setFinalContent('')

    fetch('/api/debate/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ topic, field }),
    }).then(res => {
      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      const processChunk = ({ done, value }) => {
        if (done) { setPhase('done'); return }

        buffer += decoder.decode(value, { stream: true })
        const parts = buffer.split('\n\n')
        buffer = parts.pop() // last incomplete chunk

        for (const part of parts) {
          if (!part.trim()) continue
          const eventMatch = part.match(/^event: (.+)$/m)
          const dataMatch = part.match(/^data: (.+)$/m)
          if (!eventMatch || !dataMatch) continue

          const event = eventMatch[1]
          let data
          try { data = JSON.parse(dataMatch[1]) } catch { continue }

          handleEvent(event, data)
        }

        reader.read().then(processChunk)
      }

      reader.read().then(processChunk)
    }).catch(err => {
      setStatus('Lỗi kết nối: ' + err.message)
      setPhase('setup')
    })
  }

  const handleEvent = (event, data) => {
    switch (event) {
      case 'status':
        setStatus(data.message)
        break

      case 'professors':
        setProfessors(data.professors)
        break

      case 'round':
        setTurns(t => [...t, { type: 'round', round: data.round, id: Date.now() }])
        break

      case 'moderator':
        setTurns(t => [...t, {
          type: 'moderator', label: data.label,
          content: data.content, id: Date.now(),
        }])
        break

      case 'speaker_start':
        setTurns(t => [...t, {
          type: 'professor', key: data.key, name: data.name,
          role: data.role, turn: data.turn,
          content: '', streaming: true, id: `${data.turn}-${data.key}`,
        }])
        break

      case 'chunk':
        setTurns(t => {
          const last = t[t.length - 1]
          if (!last || !last.streaming) return t
          return [...t.slice(0, -1), { ...last, content: last.content + data.text }]
        })
        break

      case 'speaker_end':
        setTurns(t => {
          const idx = t.findIndex(x => x.id === `${data.turn}-${data.key}`)
          if (idx === -1) return t
          const updated = [...t]
          updated[idx] = { ...updated[idx], streaming: false, fact_tags: data.fact_tags }
          return updated
        })
        break

      case 'final':
        setFinalContent(data.content)
        setTurns(t => [...t, { type: 'final', content: data.content, id: 'final' }])
        break

      case 'saved':
        setStatus('Đã lưu: ' + data.filename)
        break

      case 'error':
        setStatus('Lỗi: ' + data.message)
        setPhase('done')
        break
    }
  }

  if (phase === 'setup') {
    return <SetupForm onStart={startDebate} loading={false} />
  }

  return (
    <div style={styles.arena}>
      {/* Sidebar professors */}
      <aside style={styles.sidebar}>
        <div style={styles.sideTitle}>Professors</div>
        {professors.map((p, i) => (
          <ProfessorCard key={p.key} prof={p} color={PROF_COLORS[i]} />
        ))}
      </aside>

      {/* Main debate feed */}
      <main style={styles.feed}>
        <div style={styles.statusBar}>{status}</div>
        {turns.map(turn => (
          <TurnBubble key={turn.id} turn={turn} professors={professors} />
        ))}
        <div ref={bottomRef} />
      </main>
    </div>
  )
}

// ── Styles ────────────────────────────────────────────────────────────────────

const styles = {
  setupWrap: {
    maxWidth: 620, margin: '80px auto', padding: '0 20px',
  },
  logo: {
    fontSize: 28, fontWeight: 700, marginBottom: 8,
    background: 'linear-gradient(135deg, #4fc3f7, #ce93d8)',
    WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent',
  },
  subtitle: { color: '#888', marginBottom: 32, fontSize: 15 },
  form: { display: 'flex', flexDirection: 'column', gap: 12 },
  label: { fontSize: 13, color: '#aaa', marginBottom: 2 },
  input: {
    background: '#1a1d27', border: '1px solid #2e3248',
    borderRadius: 8, padding: '10px 14px', color: '#e8e8e8',
    fontSize: 14, outline: 'none', width: '100%',
  },
  btn: {
    background: 'linear-gradient(135deg, #4fc3f7, #7c4dff)',
    border: 'none', borderRadius: 8, padding: '12px 20px',
    color: '#fff', fontSize: 15, fontWeight: 600,
    cursor: 'pointer', marginTop: 8,
  },
  arena: {
    display: 'flex', height: '100vh', overflow: 'hidden',
  },
  sidebar: {
    width: 260, padding: 16, borderRight: '1px solid #2e3248',
    overflowY: 'auto', flexShrink: 0,
  },
  sideTitle: {
    fontSize: 11, fontWeight: 600, color: '#666',
    letterSpacing: '0.1em', textTransform: 'uppercase', marginBottom: 12,
  },
  profCard: {
    display: 'flex', gap: 10, padding: '10px 0',
    borderBottom: '1px solid #1e2235',
    borderLeft: '3px solid', paddingLeft: 8, marginBottom: 4,
  },
  profAvatar: {
    width: 32, height: 32, borderRadius: 8,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    fontSize: 16, flexShrink: 0,
  },
  profName: { fontSize: 13, fontWeight: 600, marginBottom: 2 },
  profUni: { fontSize: 11, color: '#666', marginBottom: 2 },
  profRole: { fontSize: 11, color: '#888' },
  profStance: { fontSize: 11, color: '#666', marginTop: 3, lineHeight: 1.4 },
  feed: {
    flex: 1, overflowY: 'auto', padding: '16px 24px', display: 'flex',
    flexDirection: 'column', gap: 12,
  },
  statusBar: {
    fontSize: 12, color: '#666', padding: '6px 0', marginBottom: 4,
  },
  roundDivider: {
    textAlign: 'center', color: '#555', fontSize: 12,
    padding: '8px 0', letterSpacing: '0.1em',
  },
  modBubble: {
    background: '#1a1f35', borderLeft: '3px solid #7c4dff',
    borderRadius: '0 8px 8px 0', padding: '12px 16px',
  },
  modLabel: { fontSize: 11, color: '#7c4dff', fontWeight: 600, marginBottom: 6 },
  modContent: { fontSize: 14, color: '#ccc', lineHeight: 1.6 },
  turnWrap: {
    borderLeft: '3px solid', paddingLeft: 14,
    paddingBottom: 4,
  },
  turnHeader: {
    display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6,
  },
  turnName: { fontSize: 14, fontWeight: 600 },
  turnRole: { fontSize: 11, color: '#666' },
  turnNum: { fontSize: 11, color: '#444', marginLeft: 'auto' },
  turnContent: { fontSize: 14, lineHeight: 1.7, color: '#ddd' },
  cursor: { animation: 'blink 1s infinite' },
  factWrap: { marginTop: 10, display: 'flex', flexDirection: 'column', gap: 4 },
  factRow: { display: 'flex', alignItems: 'baseline', gap: 6, flexWrap: 'wrap' },
  factBadge: {
    fontSize: 11, fontWeight: 600, padding: '1px 6px',
    border: '1px solid', borderRadius: 4, flexShrink: 0,
  },
  factClaim: { fontSize: 12, color: '#999' },
  factReason: { fontSize: 12, color: '#777', fontStyle: 'italic' },
  factSource: { fontSize: 11, color: '#4fc3f7', marginLeft: 8, width: '100%' },
  finalWrap: {
    background: '#0d1b14', border: '1px solid #1e3a2a',
    borderRadius: 10, padding: '16px 20px', marginTop: 8,
  },
  finalTitle: {
    fontSize: 14, fontWeight: 700, color: '#66bb6a', marginBottom: 12,
  },
  finalSection: { fontSize: 13, color: '#81c784', fontWeight: 600, marginTop: 10 },
  finalBullet: { fontSize: 13, color: '#ccc', paddingLeft: 12, marginTop: 4 },
  finalLine: { fontSize: 13, color: '#aaa', marginTop: 2 },
}
