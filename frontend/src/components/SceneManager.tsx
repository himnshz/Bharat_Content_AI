'use client'

import { Suspense, useState, useEffect } from 'react'
import { Canvas } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera, EffectComposer, Bloom } from '@react-three/drei'
import HomeScene from './scenes/HomeScene'
import GenerateScene from './scenes/GenerateScene'
import TranslateScene from './scenes/TranslateScene'

interface SceneManagerProps {
  currentScene: string
}

export default function SceneManager({ currentScene }: SceneManagerProps) {
  const [scene, setScene] = useState(currentScene)
  const [transitioning, setTransitioning] = useState(false)

  useEffect(() => {
    if (currentScene !== scene) {
      setTransitioning(true)
      
      // Smooth transition delay
      setTimeout(() => {
        setScene(currentScene)
        setTransitioning(false)
      }, 500)
    }
  }, [currentScene, scene])

  const renderScene = () => {
    switch (scene) {
      case 'generate':
        return <GenerateScene />
      case 'translate':
        return <TranslateScene />
      case 'home':
      default:
        return <HomeScene />
    }
  }

  return (
    <div 
      className={`
        w-full h-full relative
        transition-all duration-500
        ${transitioning ? 'scale-out-center opacity-50' : 'scale-in-center opacity-100'}
      `}
    >
      <Canvas
        shadows
        dpr={[1, 2]}
        gl={{ 
          antialias: true,
          alpha: true,
          powerPreference: 'high-performance'
        }}
      >
        {/* Camera */}
        <PerspectiveCamera makeDefault position={[0, 0, 8]} fov={50} />

        {/* Scene Content */}
        <Suspense fallback={null}>
          {renderScene()}
        </Suspense>

        {/* Post-processing - Bloom for that ethereal glow */}
        <EffectComposer>
          <Bloom
            intensity={0.6}
            luminanceThreshold={0.2}
            luminanceSmoothing={0.9}
            radius={0.8}
          />
        </EffectComposer>

        {/* Controls */}
        <OrbitControls
          enableZoom={false}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.3}
          maxPolarAngle={Math.PI / 1.8}
          minPolarAngle={Math.PI / 2.5}
        />
      </Canvas>

      {/* Scene Label */}
      <div className="absolute bottom-8 left-1/2 transform -translate-x-1/2 z-10">
        <div className="glass-effect px-6 py-3 rounded-full">
          <p className="text-white font-medium tracking-wider uppercase text-sm">
            {scene === 'home' && '🏠 Home Universe'}
            {scene === 'generate' && '✨ Content Generation'}
            {scene === 'translate' && '🌐 Translation Hub'}
            {scene === 'schedule' && '📅 Scheduler'}
            {scene === 'analytics' && '📊 Analytics'}
            {scene === 'voice' && '🎤 Voice Input'}
            {scene === 'profile' && '👤 Profile'}
          </p>
        </div>
      </div>

      {/* Loading overlay during transition */}
      {transitioning && (
        <div className="absolute inset-0 bg-gradient-lavender/20 backdrop-blur-sm flex items-center justify-center z-20">
          <div className="shimmer px-8 py-4 rounded-xl">
            <p className="text-white font-bold text-xl">Warping...</p>
          </div>
        </div>
      )}
    </div>
  )
}
