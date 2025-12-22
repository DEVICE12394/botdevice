import { useEffect, useState } from 'react'

function App() {
  const [user, setUser] = useState(null)
  const [inventory, setInventory] = useState([])
  const [stats, setStats] = useState({ total: 0, low_stock: 0, families: 0 })
  const [loading, setLoading] = useState(true)
  const tg = window.Telegram?.WebApp;

  useEffect(() => {
    if (tg) {
      tg.ready();
      tg.expand();
      setUser(tg.initDataUnsafe?.user);
      
      tg.MainButton.setText("🔄 Actualizar Datos");
      tg.MainButton.show();
      tg.MainButton.onClick(fetchData);
    }
    fetchData();
  }, []);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [invRes, statsRes] = await Promise.all([
        fetch('/api/inventory'),
        fetch('/api/stats')
      ]);
      const invData = await invRes.json();
      const statsData = await statsRes.json();
      
      setInventory(invData);
      setStats(statsData);
    } catch (error) {
      console.error("Error fetching data:", error);
    } finally {
      setLoading(false);
    }
  };

  const lowStockItems = inventory.filter(item => {
    const qty = parseFloat(item.quantity) || 0;
    const min = parseFloat(item.min_stock) || 0;
    return qty <= min && qty > 0;
  });

  const criticalItems = inventory.filter(item => (parseFloat(item.quantity) || 0) <= 0);

  return (
    <div className="container">
      <header style={{marginBottom: '2rem'}}>
        <div style={{fontSize: '3rem', marginBottom: '0.5rem'}}>🏭</div>
        <h1>Inventory Real-Time</h1>
        <p style={{opacity: 0.7}}>
          Bienvenido, <strong>{user?.first_name || 'Invitado'}</strong>
        </p>
      </header>

      {loading ? (
        <div style={{textAlign: 'center', padding: '2rem'}}>Cargando datos...</div>
      ) : (
        <>
          <div className="grid-2">
            <div className="card">
              <div className="stat-value">{stats.total}</div>
              <div className="stat-label">Total Items</div>
            </div>
            <div className="card">
              <div className="stat-value" style={{color: '#ff4081'}}>{criticalItems.length + lowStockItems.length}</div>
              <div className="stat-label">Alertas</div>
            </div>
          </div>

          <h3 style={{marginTop: '2rem'}}>⚠️ Alertas Críticas ({criticalItems.length})</h3>
          {criticalItems.map((item, i) => (
            <div key={i} className="card" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderLeft: '4px solid #ff4081'}}>
              <div>
                <div style={{fontWeight: 'bold', fontSize: '1.1rem'}}>{item.name}</div>
                <div style={{fontSize: '0.9rem', opacity: 0.6}}>SKU: {item.sku}</div>
              </div>
              <div className="status-badge" style={{background: '#ff4081'}}>AGOTADO</div>
            </div>
          ))}

          <h3 style={{marginTop: '2rem'}}>🟠 Stock Bajo ({lowStockItems.length})</h3>
          {lowStockItems.map((item, i) => (
            <div key={i} className="card" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderLeft: '4px solid #ff8c00'}}>
              <div>
                <div style={{fontWeight: 'bold', fontSize: '1.1rem'}}>{item.name}</div>
                <div style={{fontSize: '0.9rem', opacity: 0.6}}>SKU: {item.sku}</div>
              </div>
              <div className="status-badge status-warn">{item.quantity} {item.unit}</div>
            </div>
          ))}

          {!criticalItems.length && !lowStockItems.length && (
            <div className="card" style={{textAlign: 'center', opacity: 0.5}}>✨ Todo el stock está saludable</div>
          )}
        </>
      )}
    </div>
  )
}

export default App
