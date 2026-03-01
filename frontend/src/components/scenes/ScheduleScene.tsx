'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Text, Float } from '@react-three/drei'
import * as THREE from 'three'

export default function ScheduleScene() {
  const calendarRef = useRef<THREE.Group>(null)

  useFrame((state) => {
    const t = state.clock.getElapsedTime()

    if (calendarRef.current) {
      calendarRef.current.rotation.y = Math.sin(t * 0.3) * 0.2
    }
  })

  return (
    <>
      <fog attach="fog" args={['#8E70CF', 5, 20]} />
      
      <ambientLight intensity={0.7} color="#A4A5F5" />
      <directionalLight position={[5, 5, 5]} intensity={1.5} color="#9EF0FF" />
      <pointLight position={[0, 5, 0]} intensity={1} color="#B5C7EB" />

      {/* Calendar grid */}
      <group ref={calendarRef}>
        {[...Array(7)].map((_, i) => (
          <Float key={i} speed={1 + i * 0.1} rotationIntensity={0.2} floatIntensity={0.4}>
            <mesh position={[(i - 3) * 0.8, 0, 0]}>
              <boxGeometry args={[0.6, 0.6, 0.1]} />
              <meshStandardMaterial
                color="#B5C7EB"
                metalness={0.6}
                roughness={0.3}
                emissive="#B5C7EB"
                emissiveIntensity={0.3}
              />
            </mesh>
          </Float>
        ))}
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
          Schedule Posts
        </Text>
      </Float>
    </>
  )
}
