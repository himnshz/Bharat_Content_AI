'use client'

import { useRef, useMemo } from 'react'
import { Canvas, useFrame } from '@react-three/fiber'
import { OrbitControls, Sphere, MeshDistortMaterial, Float, Text3D, Center } from '@react-three/drei'
import * as THREE from 'three'

// Animated Sphere with distortion
function AnimatedSphere() {
  const meshRef = useRef<THREE.Mesh>(null)
  
  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.x = state.clock.getElapsedTime() * 0.2
      meshRef.current.rotation.y = state.clock.getElapsedTime() * 0.3
    }
  })

  return (
    <Float speed={2} rotationIntensity={0.5} floatIntensity={0.5}>
      <Sphere ref={meshRef} args={[1, 100, 100]} scale={2.5}>
        <MeshDistortMaterial
          color="#A4A5F5"
          attach="material"
          distort={0.4}
          speed={2}
          roughness={0.2}
          metalness={0.8}
        />
      </Sphere>
    </Float>
  )
}

// Particle system for background
function Particles() {
  const count = 500
  const positions = useMemo(() => {
    const pos = new Float32Array(count * 3)
    for (let i = 0; i < count; i++) {
      pos[i * 3] = (Math.random() - 0.5) * 20
      pos[i * 3 + 1] = (Math.random() - 0.5) * 20
      pos[i * 3 + 2] = (Math.random() - 0.5) * 20
    }
    return pos
  }, [])

  const particlesRef = useRef<THREE.Points>(null)

  useFrame((state) => {
    if (particlesRef.current) {
      particlesRef.current.rotation.y = state.clock.getElapsedTime() * 0.05
    }
  })

  return (
    <points ref={particlesRef}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={count}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <pointsMaterial
        size={0.05}
        color="#9EF0FF"
        transparent
        opacity={0.6}
        sizeAttenuation
      />
    </points>
  )
}

// Floating rings
function FloatingRings() {
  const ring1Ref = useRef<THREE.Mesh>(null)
  const ring2Ref = useRef<THREE.Mesh>(null)
  const ring3Ref = useRef<THREE.Mesh>(null)

  useFrame((state) => {
    const t = state.clock.getElapsedTime()
    if (ring1Ref.current) {
      ring1Ref.current.rotation.x = t * 0.3
      ring1Ref.current.rotation.y = t * 0.2
    }
    if (ring2Ref.current) {
      ring2Ref.current.rotation.x = t * 0.4
      ring2Ref.current.rotation.z = t * 0.3
    }
    if (ring3Ref.current) {
      ring3Ref.current.rotation.y = t * 0.5
      ring3Ref.current.rotation.z = t * 0.2
    }
  })

  return (
    <>
      <mesh ref={ring1Ref} position={[0, 0, 0]}>
        <torusGeometry args={[3, 0.05, 16, 100]} />
        <meshStandardMaterial color="#B5C7EB" transparent opacity={0.3} />
      </mesh>
      <mesh ref={ring2Ref} position={[0, 0, 0]}>
        <torusGeometry args={[3.5, 0.05, 16, 100]} />
        <meshStandardMaterial color="#9EF0FF" transparent opacity={0.3} />
      </mesh>
      <mesh ref={ring3Ref} position={[0, 0, 0]}>
        <torusGeometry args={[4, 0.05, 16, 100]} />
        <meshStandardMaterial color="#8E70CF" transparent opacity={0.3} />
      </mesh>
    </>
  )
}

// Main 3D Scene
export default function Hero3D() {
  return (
    <div className="w-full h-[600px] relative">
      <Canvas
        camera={{ position: [0, 0, 8], fov: 50 }}
        style={{ background: 'transparent' }}
      >
        {/* Lighting */}
        <ambientLight intensity={0.5} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <pointLight position={[-10, -10, -5]} intensity={0.5} color="#9EF0FF" />
        <pointLight position={[10, 10, 10]} intensity={0.5} color="#A4A5F5" />

        {/* 3D Elements */}
        <Particles />
        <FloatingRings />
        <AnimatedSphere />

        {/* Controls */}
        <OrbitControls
          enableZoom={false}
          enablePan={false}
          autoRotate
          autoRotateSpeed={0.5}
          maxPolarAngle={Math.PI / 2}
          minPolarAngle={Math.PI / 2}
        />
      </Canvas>
    </div>
  )
}
