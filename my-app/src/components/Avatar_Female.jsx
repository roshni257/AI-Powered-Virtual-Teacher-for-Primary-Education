import React, { useRef, useEffect } from 'react'
import { useGraph } from '@react-three/fiber'
import { useFBX, useGLTF, useAnimations } from '@react-three/drei'
import { SkeletonUtils } from 'three-stdlib'
import * as THREE from 'three'

export function Avatar_Female(props) {
  const { isSpeaking } = props;
  const group = useRef();
  
  const { scene } = useGLTF('/models/teacher_female.glb')
  const idleFBX = useFBX('/animations/Idle_Standing_female.fbx')
  const talkingFBX = useFBX('/animations/Talking_Standing_female.fbx')

  // Clone the scene
  const clone = React.useMemo(() => SkeletonUtils.clone(scene), [scene])
  const { nodes, materials } = useGraph(clone)

  // Process and retarget animations
  const animations = React.useMemo(() => {
    const processedAnims = [];
    
    if (idleFBX.animations && idleFBX.animations[0]) {
      const idle = idleFBX.animations[0].clone();
      idle.name = "Idle";
      
      // Retarget animation tracks to match RPM skeleton
      idle.tracks = idle.tracks.map(track => {
        // Remove mixamorig prefix if present
        const newName = track.name.replace('mixamorig', '');
        return new THREE.KeyframeTrack(
          newName,
          track.times,
          track.values,
          track.interpolation
        );
      });
      
      processedAnims.push(idle);
    }
    
    if (talkingFBX.animations && talkingFBX.animations[0]) {
      const talking = talkingFBX.animations[0].clone();
      talking.name = "Talking";
      
      // Retarget animation tracks
      talking.tracks = talking.tracks.map(track => {
        const newName = track.name.replace('mixamorig', '');
        return new THREE.KeyframeTrack(
          newName,
          track.times,
          track.values,
          track.interpolation
        );
      });
      
      processedAnims.push(talking);
    }
    
    return processedAnims;
  }, [idleFBX.animations, talkingFBX.animations]);

  const { actions, mixer } = useAnimations(animations, group);

  // Debug: Log available actions
  useEffect(() => {
    console.log('Available actions:', Object.keys(actions));
    console.log('Mixer:', mixer);
    console.log('Animations:', animations);
  }, [actions, mixer, animations]);

  useEffect(() => {
    if (!actions || Object.keys(actions).length === 0) {
      console.warn('No actions available');
      return;
    }

    const animationName = isSpeaking ? "Talking" : "Idle";
    console.log('Trying to play:', animationName, 'isSpeaking:', isSpeaking);
    
    // Stop all actions
    Object.values(actions).forEach(action => {
      if (action) {
        action.stop();
        action.reset();
      }
    });

    // Play the selected action
    const action = actions[animationName];
    if (action) {
      console.log('Playing action:', animationName);
      action.setLoop(THREE.LoopRepeat);
      action.clampWhenFinished = false;
      action.reset().fadeIn(0.5).play();
    } else {
      console.warn('Action not found:', animationName);
    }

    return () => {
      if (action) {
        action.fadeOut(0.5);
      }
    };
  }, [isSpeaking, actions]);

  return (
    <group {...props} dispose={null} ref={group}>
      <primitive object={nodes.Hips} />
      <skinnedMesh 
        geometry={nodes.Wolf3D_Hair.geometry} 
        material={materials.Wolf3D_Hair} 
        skeleton={nodes.Wolf3D_Hair.skeleton} 
      />
      <skinnedMesh 
        geometry={nodes.Wolf3D_Glasses.geometry} 
        material={materials.Wolf3D_Glasses} 
        skeleton={nodes.Wolf3D_Glasses.skeleton} 
      />
      <skinnedMesh 
        geometry={nodes.Wolf3D_Body.geometry} 
        material={materials.Wolf3D_Body} 
        skeleton={nodes.Wolf3D_Body.skeleton} 
      />
      <skinnedMesh 
        geometry={nodes.Wolf3D_Outfit_Bottom.geometry} 
        material={materials.Wolf3D_Outfit_Bottom} 
        skeleton={nodes.Wolf3D_Outfit_Bottom.skeleton} 
      />
      <skinnedMesh 
        geometry={nodes.Wolf3D_Outfit_Footwear.geometry} 
        material={materials.Wolf3D_Outfit_Footwear} 
        skeleton={nodes.Wolf3D_Outfit_Footwear.skeleton} 
      />
      <skinnedMesh 
        geometry={nodes.Wolf3D_Outfit_Top.geometry} 
        material={materials.Wolf3D_Outfit_Top} 
        skeleton={nodes.Wolf3D_Outfit_Top.skeleton} 
      />
      <skinnedMesh 
        name="EyeLeft" 
        geometry={nodes.EyeLeft.geometry} 
        material={materials.Wolf3D_Eye} 
        skeleton={nodes.EyeLeft.skeleton} 
        morphTargetDictionary={nodes.EyeLeft.morphTargetDictionary} 
        morphTargetInfluences={nodes.EyeLeft.morphTargetInfluences} 
      />
      <skinnedMesh 
        name="EyeRight" 
        geometry={nodes.EyeRight.geometry} 
        material={materials.Wolf3D_Eye} 
        skeleton={nodes.EyeRight.skeleton} 
        morphTargetDictionary={nodes.EyeRight.morphTargetDictionary} 
        morphTargetInfluences={nodes.EyeRight.morphTargetInfluences} 
      />
      <skinnedMesh 
        name="Wolf3D_Head" 
        geometry={nodes.Wolf3D_Head.geometry} 
        material={materials.Wolf3D_Skin} 
        skeleton={nodes.Wolf3D_Head.skeleton} 
        morphTargetDictionary={nodes.Wolf3D_Head.morphTargetDictionary} 
        morphTargetInfluences={nodes.Wolf3D_Head.morphTargetInfluences} 
      />
      <skinnedMesh 
        name="Wolf3D_Teeth" 
        geometry={nodes.Wolf3D_Teeth.geometry} 
        material={materials.Wolf3D_Teeth} 
        skeleton={nodes.Wolf3D_Teeth.skeleton} 
        morphTargetDictionary={nodes.Wolf3D_Teeth.morphTargetDictionary} 
        morphTargetInfluences={nodes.Wolf3D_Teeth.morphTargetInfluences} 
      />
    </group>
  )
}

useGLTF.preload('/models/teacher_female.glb')
useFBX.preload('/animations/Idle_Standing_female.fbx')
useFBX.preload('/animations/Talking_Standing_female.fbx')