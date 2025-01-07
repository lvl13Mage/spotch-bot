import { createRoot } from 'react-dom/client';
import AppMain from './components/AppMain';
import './styles/styles.css';


const root = createRoot(document.querySelector('#root'));
root.render(<AppMain />);