'use client'

import { useRef, useMemo } from 'react'
import { useFrame } from '@react-three/fiber'
import { Sphere, MeshDistortMaterial, Float, Stars } from '@react-three/drei'
import * as THREE from 'three'

export default function HomeScene() {
  const sphereRef = useRef<THREE.Mesh>(null)
  const ringsRef = useRef<THREE.Group>(null)

  // Floating particles
  const particles = useMemo(() => {
    const count = 500
    const positions = new Float32Array(count * 3)
    const colors = new Float32Array(count * 3)
    
    const lavenderColors = [
      new THREE.Color('#B5C7EB'),
      new THREE.Color('#9EF0FF'),
      new THREE.Color('#A4A5F5'),
      new THREE.Color('#8E70CF'),
    ]

    for (let i = 0; i < count; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 20
      positions[i * 3 + 1] = (Math.random() - 0.5) * 20
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20

      const color = lavenderColors[Math.floor(Math.random() * lavenderColors.length)]
      colors[i * 3] = color.r
      colors[i * 3 + 1] = color.g
      colors[i * 3 + 2] = color.b
    }

    return { positions, colors }
  }, [])

  useFrame((state) => {
    const t = state.clock.getElapsedTime()

    // Gentle breathing motion for sphere
    if (sphereRef.current) {
      sphereRef.current.position.y = Math.sin(t * 0.5) * 0.3
      sphereRef.current.rotation.x = t * 0.1
      sphereRef.current.rotation.y = t * 0.15
    }

    // Slow rotation for rings
    if (ringsRef.current) {
      ringsRef.current.rotation.x = t * 0.1
      ringsRef.current.rotation.y = t * 0.2
    }
  })

  return (
    <>
      {/* Ambient fog */}
      <fog attach="fog" args={['#A4A5F5', 8, 25]} />

      {/* Lighting - Lavender Glow */}
      <ambientLight intensity={0.8} color="#9ef0ff" />
      <directionalLight position={[5, 5, 5]} intensity={1.5} color="#8e70cf" />
      <pointLight position={[-10, -10, -5]} intensity={0.5} color="#9EF0FF" />
      <pointLight position={[10, 10, 10]} intensity={0.5} color="#A4A5F5" />

      {/* Stars background */}
      <Stars 
        radius={100} 
        depth={50} 
        count={3000} 
        factor={4} 
        saturation={0.5} 
        fade 
        speed={0.5}
      />

      {/* Floating particles */}
      <points>
        <bufferGeometry>
          <bufferAttribute
            attach="attributes-position"
            count={particles.positions.length / 3}
            array={particles.positions}
            itemSize={3}
          />
          <bufferAttribute
            attach="attributes-color"
            count={particles.colors.length / 3}
            array={particles.colors}
            itemSize={3}
          />
        </bufferGeometry>
        <pointsMaterial
          size={0.05}
          vertexColors
          transparent
          opacity={0.6}
          sizeAttenuation
          blending={THREE.AdditiveBlending}
        />
      </points>

      {/* Main sphere - Lavender Dream */}
      <Float speed={2} rotationIntensity={0.3} floatIntensity={0.5}>
        <Sphere ref={sphereRef} args={[1.5, 100, 100]}>
          <MeshDistortMaterial
            color="#A4A5F5"
            attach="material"
            distort={0.4}
            speed={2}
            roughness={0.2}
            metalness={0.8}
            emissive="#9ef0ff"
            emissiveIntensity={0.2}
          />
        </Sphere>
      </Float>

      {/* Floating rings */}
      <group ref={ringsRef}>
        <mesh rotation={[Math.PI / 4, 0, 0]}>
          <torusGeometry args={[3, 0.05, 16, 100]} />
          <meshStandardMaterial 
            color="#B5C7EB" 
            transparent 
            opacity={0.3}
            emissive="#B5C7EB"
            emissiveIntensity={0.2}
          />
        </mesh>
        <mesh rotation={[Math.PI / 3, Math.PI / 4, 0]}>
          <torusGeometry args={[3.5, 0.05, 16, 100]} />
          <meshStandardMaterial 
            color="#9EF0FF" 
            transparent 
            opacity={0.3}
            emissive="#9EF0FF"
            emissiveIntensity={0.2}
          />
        </mesh>
        <mesh rotation={[0, Math.PI / 2, Math.PI / 4]}>
          <torusGeometry args={[4, 0.05, 16, 100]} />
          <meshStandardMaterial 
            color="#8E70CF" 
            transparent 
            opacity={0.3}
            emissive="#8E70CF"
            emissiveIntensity={0.2}
          />
        </mesh>
      </group>
    </>
  )
}
