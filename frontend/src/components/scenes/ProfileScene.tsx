'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Text, Float, Sphere, Torus } from '@react-three/drei'
import * as THREE from 'three'

export default function ProfileScene() {
  const avatarRef = useRef<THREE.Mesh>(null)
  const ringRef = useRef<THREE.Mesh>(null)

  useFrame((state) => {
    const t = state.clock.getElapsedTime()

    if (avatarRef.current) {
      avatarRef.current.position.y = Math.sin(t * 0.5) * 0.2
    }

    if (ringRef.current) {
      ringRef.current.rotation.z = t * 0.5
    }
  })

  return (
    <>
      <fog attach="fog" args={['#8E70CF', 5, 20]} />
      
      <ambientLight intensity={0.7} color="#8E70CF" />
      <directionalLight position={[5, 5, 5]} intensity={1.5} color="#9EF0FF" />
      <pointLight position={[0, 0, 5]} intensity={1} color="#A4A5F5" />

      {/* Avatar sphere */}
      <Float speed={1.5} rotationIntensity={0.2} floatIntensity={0.4}>
        <Sphere ref={avatarRef} args={[1, 64, 64]}>
          <meshStandardMaterial
            color="#8E70CF"
            metalness={0.8}
            roughness={0.2}
            emissive="#8E70CF"
            emissiveIntensity={0.3}
          />
        </Sphere>
      </Float>

      {/* Rotating ring around avatar */}
      <mesh ref={ringRef}>
        <torusGeometry args={[1.5, 0.05, 16, 100]} />
        <meshStandardMaterial
          color="#9EF0FF"
          transparent
          opacity={0.6}
          emissive="#9EF0FF"
          emissiveIntensity={0.4}
        />
      </mesh>

      {/* Central text */}
      <Float speed={1} floatIntensity={0.3}>
        <Text
          position={[0, -2.5, 0]}
          fontSize={0.4}
          color="#FFFFFF"
          anchorX="center"
          anchorY="middle"
        >
          Profile
        </Text>
      </Float>
    </>
  )
}
