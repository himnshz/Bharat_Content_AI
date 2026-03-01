'use client'

import { useRef } from 'react'
import { useFrame } from '@react-three/fiber'
import { Text, Float, Trail } from '@react-three/drei'
import * as THREE from 'three'

export default function TranslateScene() {
  const orbsRef = useRef<THREE.Group>(null)

  useFrame((state) => {
    const t = state.clock.getElapsedTime()

    if (orbsRef.current) {
      orbsRef.current.children.forEach((child, i) => {
        const offset = (i / orbsRef.current!.children.length) * Math.PI * 2
        child.position.x = Math.cos(t * 0.5 + offset) * 3
        child.position.z = Math.sin(t * 0.5 + offset) * 3
        child.position.y = Math.sin(t * 0.3 + offset) * 0.5
      })
    }
  })

  const languages = ['हिं', 'த', 'తె', 'বা', 'ગુ']

  return (
    <>
      <fog attach="fog" args={['#B5C7EB', 5, 20]} />
      
      <ambientLight intensity={0.7} color="#B5C7EB" />
      <directionalLight position={[5, 5, 5]} intensity={1.5} color="#9EF0FF" />
      <pointLight position={[-5, 0, 0]} intensity={1} color="#A4A5F5" />

      {/* Orbiting language spheres */}
      <group ref={orbsRef}>
        {languages.map((lang, i) => (
          <Float key={i} speed={1.5} rotationIntensity={0.3} floatIntensity={0.5}>
            <mesh>
              <sphereGeometry args={[0.4, 32, 32]} />
              <meshStandardMaterial
                color="#8E70CF"
                metalness={0.7}
                roughness={0.3}
                emissive="#8E70CF"
                emissiveIntensity={0.4}
              />
            </mesh>
            <Text
              position={[0, 0, 0.5]}
              fontSize={0.3}
              color="#FFFFFF"
              anchorX="center"
              anchorY="middle"
            >
              {lang}
            </Text>
          </Float>
        ))}
      </group>

      {/* Central connector */}
      <mesh>
        <torusGeometry args={[3, 0.1, 16, 100]} />
        <meshStandardMaterial
          color="#9EF0FF"
          transparent
          opacity={0.4}
          emissive="#9EF0FF"
          emissiveIntensity={0.3}
        />
      </mesh>
    </>
  )
}
