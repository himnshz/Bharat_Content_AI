'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Text, Float } from '@react-three/drei'
import * as THREE from 'three'

export default function AnalyticsScene() {
  const barsRef = useRef<THREE.Group>(null)

  useFrame((state) => {
    const t = state.clock.getElapsedTime()

    if (barsRef.current) {
      barsRef.current.children.forEach((child, i) => {
        const scale = 1 + Math.sin(t + i) * 0.2
        child.scale.y = scale
      })
    }
  })

  return (
    <>
      <fog attach="fog" args={['#9EF0FF', 5, 20]} />
      
      <ambientLight intensity={0.7} color="#9EF0FF" />
      <directionalLight position={[5, 5, 5]} intensity={1.5} color="#A4A5F5" />
      <pointLight position={[0, 0, 5]} intensity={1} color="#8E70CF" />

      {/* Bar chart */}
      <group ref={barsRef}>
        {[...Array(5)].map((_, i) => {
          const height = 1 + i * 0.3
          return (
            <mesh key={i} position={[(i - 2) * 1, height / 2, 0]}>
              <boxGeometry args={[0.6, height, 0.6]} />
              <meshStandardMaterial
                color="#9EF0FF"
                metalness={0.7}
                roughness={0.2}
                emissive="#9EF0FF"
                emissiveIntensity={0.4}
              />
            </mesh>
          )
        })}
      </group>

      {/* Central text */}
      <Float speed={1} floatIntensity={0.3}>
        <Text
          position={[0, -2, 0]}
          fontSize={0.4}
          color="#FFFFFF"
          anchorX="center"
          anchorY="middle"
        >
          Analytics
        </Text>
      </Float>
    </>
  )
}
