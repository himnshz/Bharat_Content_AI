'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Text, Float, Sphere } from '@react-three/drei'
import * as THREE from 'three'

export default function VoiceScene() {
  const waveRef = useRef<THREE.Group>(null)

  useFrame((state) => {
    const t = state.clock.getElapsedTime()

    if (waveRef.current) {
      waveRef.current.children.forEach((child, i) => {
        const offset = i * 0.5
        child.position.y = Math.sin(t * 2 + offset) * 0.5
      })
    }
  })

  return (
    <>
      <fog attach="fog" args={['#A4A5F5', 5, 20]} />
      
      <ambientLight intensity={0.7} color="#A4A5F5" />
      <directionalLight position={[5, 5, 5]} intensity={1.5} color="#9EF0FF" />
      <pointLight position={[0, 0, 5]} intensity={1} color="#8E70CF" />

      {/* Sound wave visualization */}
      <group ref={waveRef}>
        {[...Array(10)].map((_, i) => (
          <Sphere key={i} args={[0.2, 32, 32]} position={[(i - 4.5) * 0.8, 0, 0]}>
            <meshStandardMaterial
              color="#A4A5F5"
              metalness={0.8}
              roughness={0.2}
              emissive="#A4A5F5"
              emissiveIntensity={0.5}
            />
          </Sphere>
        ))}
      </group>

      {/* Central microphone icon representation */}
      <Float speed={1.5} rotationIntensity={0.3} floatIntensity={0.5}>
        <mesh position={[0, 0, 0]}>
          <capsuleGeometry args={[0.3, 0.8, 16, 32]} />
          <meshStandardMaterial
            color="#9EF0FF"
            metalness={0.9}
            roughness={0.1}
            emissive="#9EF0FF"
            emissiveIntensity={0.4}
          />
        </mesh>
      </Float>

      {/* Central text */}
      <Float speed={1} floatIntensity={0.3}>
        <Text
          position={[0, -2, 0]}
          fontSize={0.4}
          color="#FFFFFF"
          anchorX="center"
          anchorY="middle"
        >
          Voice Input
        </Text>
      </Float>
    </>
  )
}
