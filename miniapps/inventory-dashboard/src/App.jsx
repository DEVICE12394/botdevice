import { useEffect, useState } from 'react'

function App() {
  const [user, setUser] = useState(null)
  const tg = window.Telegram?.WebApp;

  useEffect(() => {
    if (tg) {
      tg.ready();
      tg.expand(); // Ocupar toda la pantalla
      
      const userInfo = tg.initDataUnsafe?.user;
      if (userInfo) {
        setUser(userInfo);
      }
      
      // Configurar botón principal (Nativo de Telegram)
      tg.MainButton.setText("📦 Escanear Nuevo Item");
      tg.MainButton.show();
      tg.MainButton.onClick(() => {
        tg.showPopup({
            title: 'Escanear',
            message: 'Funcionalidad de cámara próximamente...',
            buttons: [{type: 'ok'}]
        });
      });
    }
  }, [tg]);

  return (
    <div className="container">
      <header style={{marginBottom: '2rem'}}>
        <div style={{fontSize: '3rem', marginBottom: '0.5rem'}}>🏭</div>
        <h1>Inventory AI</h1>
        <p style={{opacity: 0.7}}>
          Bienvenido, <strong>{user?.first_name || 'Invitado'}</strong>
        </p>
      </header>

      <div className="grid-2">
        <div className="card">
          <div className="stat-value">1,240</div>
          <div className="stat-label">Total Items</div>
        </div>
        <div className="card">
          <div className="stat-value" style={{color: '#ff4081'}}>8</div>
          <div className="stat-label">Alertas</div>
        </div>
      </div>

      <h3 style={{marginTop: '2rem'}}>⚠️ Atención Requerida</h3>
      
      <div className="card" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div>
          <div style={{fontWeight: 'bold', fontSize: '1.1rem'}}>Cable UTP Cat6</div>
          <div style={{fontSize: '0.9rem', opacity: 0.6}}>SKU: CAB-001</div>
        </div>
        <div className="status-badge status-warn">
          Low: 5m
        </div>
      </div>

      <div className="card" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
        <div>
          <div style={{fontWeight: 'bold', fontSize: '1.1rem'}}>Conector RJ45</div>
          <div style={{fontSize: '0.9rem', opacity: 0.6}}>SKU: CON-RJ45</div>
        </div>
        <div className="status-badge status-warn">
          Low: 20 un
        </div>
      </div>

      <div className="card">
        <h3>📊 Resumen de Familias</h3>
        <div style={{
            height: '8px', 
            background: '#333', 
            borderRadius: '4px', 
            marginTop: '1rem',
            overflow: 'hidden',
            display: 'flex'
        }}>
            <div style={{width: '60%', background: '#646cff'}}></div>
            <div style={{width: '30%', background: '#ff8c00'}}></div>
            <div style={{width: '10%', background: '#ff0080'}}></div>
        </div>
        <div style={{display:'flex', gap:'1rem', marginTop:'0.5rem', fontSize:'0.8rem', opacity:0.7}}>
            <span>🔵 Eléctrico</span>
            <span>🟠 Mecánico</span>
            <span>🔴 Otros</span>
        </div>
      </div>

    </div>
  )
}

export default App
