'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Text, Float, Sparkles } from '@react-three/drei'
import * as THREE from 'three'

export default function GenerateScene() {
  const groupRef = useRef<THREE.Group>(null)
  const particlesRef = useRef<THREE.Points>(null)

  useFrame((state) => {
    const t = state.clock.getElapsedTime()

    if (groupRef.current) {
      groupRef.current.rotation.y = t * 0.2
    }

    if (particlesRef.current) {
      particlesRef.current.rotation.y = t * 0.1
    }
  })

  return (
    <>
      <fog attach="fog" args={['#9EF0FF', 5, 20]} />
      
      <ambientLight intensity={0.6} color="#A4A5F5" />
      <directionalLight position={[10, 10, 5]} intensity={2} color="#9EF0FF" />
      <pointLight position={[0, 0, 5]} intensity={1} color="#8E70CF" />

      {/* Sparkles effect */}
      <Sparkles
        count={200}
        scale={10}
        size={3}
        speed={0.4}
        color="#9EF0FF"
      />

      {/* Floating cubes representing content generation */}
      <group ref={groupRef}>
        {[...Array(8)].map((_, i) => {
          const angle = (i / 8) * Math.PI * 2
          const radius = 3
          const x = Math.cos(angle) * radius
          const z = Math.sin(angle) * radius

          return (
            <Float key={i} speed={2 + i * 0.2} rotationIntensity={0.5} floatIntensity={0.8}>
              <mesh position={[x, Math.sin(i) * 0.5, z]}>
                <boxGeometry args={[0.5, 0.5, 0.5]} />
                <meshStandardMaterial
                  color={i % 2 === 0 ? '#A4A5F5' : '#9EF0FF'}
                  metalness={0.8}
                  roughness={0.2}
                  emissive={i % 2 === 0 ? '#A4A5F5' : '#9EF0FF'}
                  emissiveIntensity={0.3}
                />
              </mesh>
            </Float>
          )
        })}
      </group>

      {/* Central text */}
      <Float speed={1} floatIntensity={0.3}>
        <Text
          position={[0, 0, 0]}
          fontSize={0.5}
          color="#FFFFFF"
          anchorX="center"
          anchorY="middle"
        >
          AI Generate
        </Text>
      </Float>
    </>
  )
}
