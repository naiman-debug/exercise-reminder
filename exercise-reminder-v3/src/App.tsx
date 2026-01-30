import { useEffect, useState } from 'react';
import Home from './pages/Home';
import Settings from './pages/Settings';
import ReminderModal from './pages/ReminderModal';
import Celebration from './pages/Celebration';

function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || '#/');

  useEffect(() => {
    const handleHashChange = () => {
      setCurrentHash(window.location.hash || '#/');
    };

    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  const renderPage = () => {
    switch (currentHash) {
      case '#/':
      case '#':
        return <Home />;
      case '#/settings':
        return <Settings />;
      case '#/reminder':
        return <ReminderModal />;
      case '#/celebration':
        return <Celebration />;
      default:
        return <Home />;
    }
  };

  return <div className="App">{renderPage()}</div>;
}

export default App;
