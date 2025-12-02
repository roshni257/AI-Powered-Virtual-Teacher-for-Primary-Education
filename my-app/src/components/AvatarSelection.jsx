import React from 'react';

const styles = {
  overlay: {
    position: 'fixed',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.8)',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    zIndex: 1000,
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
  },
  selectionCard: {
    backgroundColor: 'white',
    borderRadius: '20px',
    padding: '40px',
    textAlign: 'center',
    boxShadow: '0 20px 40px rgba(0, 0, 0, 0.3)',
    maxWidth: '500px',
    width: '90%'
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: '700',
    marginBottom: '30px',
    background: 'linear-gradient(45deg, #667eea, #764ba2)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text'
  },
  avatarGrid: {
    display: 'flex',
    gap: '20px',
    justifyContent: 'center',
    flexWrap: 'wrap',
    marginTop: '30px'
  },
  avatarOption: {
    padding: '20px 30px',
    borderRadius: '15px',
    border: '3px solid #e1e8ff',
    backgroundColor: '#f8f9ff',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    minWidth: '180px',
    textAlign: 'center'
  },
  avatarOptionHover: {
    transform: 'translateY(-5px)',
    borderColor: '#667eea',
    boxShadow: '0 10px 25px rgba(102, 126, 234, 0.3)',
    backgroundColor: '#ffffff'
  },
  avatarIcon: {
    fontSize: '3rem',
    marginBottom: '10px'
  },
  avatarName: {
    fontSize: '1.2rem',
    fontWeight: '600',
    color: '#2c3e50',
    marginBottom: '5px'
  },
  avatarDesc: {
    fontSize: '0.9rem',
    color: '#718096'
  }
};

const AvatarSelection = ({ onAvatarSelect }) => {
  const [hoveredAvatar, setHoveredAvatar] = React.useState(null);

  const avatars = [
    {
      id: 'female',
      name: '👩‍🏫 Ms. Shanti',
      description: 'Female Teacher',
      icon: '👩‍🏫'
    },
    {
      id: 'male',
      name: '👨‍🏫 Mr. Raj',
      description: 'Male Teacher',
      icon: '👨‍🏫'
    }
  ];

  return (
    <div style={styles.overlay}>
      <div style={styles.selectionCard}>
        <h1 style={styles.title}>Choose your AI Teacher</h1>
        <p style={{ fontSize: '1.1rem', color: '#4a5568', marginBottom: '20px' }}>
          Select your preferred teacher avatar
        </p>

        <div style={styles.avatarGrid}>
          {avatars.map(avatar => (
            <div
              key={avatar.id}
              style={{
                ...styles.avatarOption,
                ...(hoveredAvatar === avatar.id ? styles.avatarOptionHover : {})
              }}
              onClick={() => onAvatarSelect(avatar.id)}
              onMouseEnter={() => setHoveredAvatar(avatar.id)}
              onMouseLeave={() => setHoveredAvatar(null)}
            >
              <div style={styles.avatarIcon}>{avatar.icon}</div>
              <div style={styles.avatarName}>{avatar.name}</div>
              <div style={styles.avatarDesc}>{avatar.description}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default AvatarSelection;