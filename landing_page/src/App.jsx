import React from 'react';
import { motion } from 'framer-motion';
import { Search, Download, Layout, Zap, Shield, Globe } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description }) => (
  <motion.div
    whileHover={{ y: -10 }}
    className="bg-white p-8 rounded-2xl shadow-xl shadow-sky-100 border border-sky-50"
  >
    <div className="bg-sky-100 w-12 h-12 rounded-lg flex items-center justify-center mb-6">
      <Icon className="text-sky-600" size={24} />
    </div>
    <h3 className="text-xl font-bold text-sky-900 mb-4">{title}</h3>
    <p className="text-sky-700 leading-relaxed">{description}</p>
  </motion.div>
);

function App() {
  return (
    <div className="min-h-screen bg-sky-50 text-sky-900">
      {/* Navigation */}
      <nav className="flex justify-between items-center px-8 py-6 max-w-7xl mx-auto">
        <div className="text-2xl font-black text-sky-600 tracking-tighter">
          VISUALES <span className="text-sky-400">UCLV</span>
        </div>
        <div className="space-x-8 font-medium">
          <a href="#features" className="hover:text-sky-500 transition-colors">Características</a>
          <a href="#download" className="bg-sky-600 text-white px-6 py-2 rounded-full hover:bg-sky-700 transition-all shadow-lg shadow-sky-200">Descargar</a>
        </div>
      </nav>

      {/* Hero Section */}
      <header className="max-w-7xl mx-auto px-8 py-24 flex flex-col items-center text-center">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
        >
          <h1 className="text-6xl md:text-7xl font-black mb-8 tracking-tight text-sky-950">
            Tu contenido favorito <br />
            <span className="text-sky-500">al alcance de un clic</span>
          </h1>
          <p className="text-xl text-sky-700 max-w-2xl mx-auto mb-12 leading-loose">
            Explora la vasta biblioteca de Visuales UCLV con una interfaz moderna,
            búsquedas instantáneas y un gestor de descargas diseñado para la velocidad.
          </p>
          <div className="flex gap-4 justify-center">
            <a href="#download" className="bg-sky-600 text-white px-10 py-4 rounded-xl font-bold text-lg hover:bg-sky-700 transition-all shadow-xl shadow-sky-200">
              Obtener Explorer
            </a>
            <a href="#features" className="bg-white text-sky-600 border-2 border-sky-100 px-10 py-4 rounded-xl font-bold text-lg hover:border-sky-300 transition-all">
              Saber más
            </a>
          </div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.3, duration: 0.8 }}
          className="mt-20 w-full max-w-5xl rounded-3xl overflow-hidden shadow-2xl shadow-sky-200 border-8 border-white"
        >
          <img
            src="https://github.com/JalexCode/VisualesUCLV-Desktop/blob/master/screenshots/main.png?raw=true"
            alt="Aplicación Visuales UCLV Explorer"
            className="w-full object-cover"
          />
        </motion.div>
      </header>

      {/* Features Section */}
      <section id="features" className="max-w-7xl mx-auto px-8 py-32">
        <div className="text-center mb-20">
          <h2 className="text-4xl font-black text-sky-950 mb-4">Potencia y Simplicidad</h2>
          <p className="text-sky-700 text-lg">Diseñado para ofrecer la mejor experiencia de navegación local.</p>
        </div>

        <div className="grid md:grid-cols-3 gap-8">
          <FeatureCard
            icon={Search}
            title="Búsqueda Inteligente"
            description="Encuentra películas, series y documentales al instante con nuestro motor de búsqueda difusa de alto rendimiento."
          />
          <FeatureCard
            icon={Zap}
            title="Rendimiento Óptimo"
            description="Navegación ultra rápida gracias al sistema de caché local y peticiones asíncronas que no bloquean la interfaz."
          />
          <FeatureCard
            icon={Download}
            title="Gestor de Descargas"
            description="Descargas resilientes con soporte para reanudación automática y múltiples tareas simultáneas."
          />
          <FeatureCard
            icon={Layout}
            title="Interfaz Moderna"
            description="Una estética limpia y profesional construida con PySide6 y Material Design para Windows y Linux."
          />
          <FeatureCard
            icon={Shield}
            title="Estabilidad Garantizada"
            description="Arquitectura limpia que asegura un funcionamiento robusto sin cierres inesperados ni errores silenciosos."
          />
          <FeatureCard
            icon={Globe}
            title="Acceso Directo"
            description="Conéctate directamente al repositorio de Visuales UCLV sin necesidad de utilizar navegadores pesados."
          />
        </div>
      </section>

      {/* Download Section */}
      <section id="download" className="bg-sky-600 py-32 text-center text-white">
        <div className="max-w-4xl mx-auto px-8">
          <h2 className="text-5xl font-black mb-8 tracking-tight">Listo para empezar</h2>
          <p className="text-xl text-sky-100 mb-12 leading-relaxed">
            Descarga la última versión de Visuales UCLV Explorer y lleva tu experiencia de navegación al siguiente nivel.
            Disponible de forma gratuita para Windows y Linux.
          </p>
          <div className="flex flex-wrap justify-center gap-6">
            <button className="bg-white text-sky-600 px-12 py-4 rounded-2xl font-black text-xl hover:bg-sky-50 transition-all shadow-2xl">
              Descargar para Windows
            </button>
            <button className="bg-sky-500 text-white border-2 border-sky-400 px-12 py-4 rounded-2xl font-black text-xl hover:bg-sky-400 transition-all">
              Descargar para Linux
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-16 text-center text-sky-700 font-medium">
        <div className="mb-4 text-sky-900 font-black tracking-tighter">
          VISUALES <span className="text-sky-500">UCLV</span>
        </div>
        <p>Desarrollado con pasión para la comunidad de UCLV.</p>
        <p className="mt-2 text-sm opacity-60">© 2025 Visuales UCLV Explorer. Todos los derechos reservados.</p>
      </footer>
    </div>
  );
}

export default App;
