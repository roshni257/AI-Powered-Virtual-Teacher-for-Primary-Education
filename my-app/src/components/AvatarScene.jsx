
import { Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import TeacherAvatar from './TeacherAvatar.jsx';

const AvatarScene = ({ gender, isSpeaking, lipsyncData, audioTime }) => {
  return (
    <div style={{
      width: '350px',
      height: '500px',
      background: 'transparent',
      borderRadius: '15px',
      overflow: 'visible',
      filter: 'drop-shadow(0 10px 30px rgba(0, 0, 0, 0.15))'
    }}>
      <Canvas style={{ background: 'transparent' }}>
        <PerspectiveCamera makeDefault position={[0, -2.5, 1.5]} fov={42} />

        {/* Enhanced lighting */}
        <ambientLight intensity={1.4} />
        <directionalLight position={[2, 4, 3]} intensity={2.2} castShadow />
        <directionalLight position={[-2, 2, -2]} intensity={0.8} />
        <spotLight 
          position={[0, 4, 1.5]} 
          intensity={1.2} 
          angle={0.5} 
          penumbra={0.3}
        />
        <pointLight position={[0, 1.5, 2]} intensity={0.5} />

        <Suspense fallback={
          <mesh>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color="orange" />
          </mesh>
        }>
          <TeacherAvatar
            key={gender}
            gender={gender}
            isSpeaking={isSpeaking}
            lipsyncData={lipsyncData}
            audioTime={audioTime}
            position={[0, 0, 0]}
            scale={1.5}
          />
        </Suspense>

        <OrbitControls
          enableZoom={false}
          enablePan={false}
          target={[0, 1.4, 0]}
          maxPolarAngle={Math.PI / 2.2}
          minPolarAngle={Math.PI / 3.5}
          maxAzimuthAngle={Math.PI / 4}
          minAzimuthAngle={-Math.PI / 4}
        />
      </Canvas>
    </div>
  );
};

export default AvatarScene;