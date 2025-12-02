
import { useState, useEffect, useRef } from "react";
import AvatarSelection from "./components/AvatarSelection.jsx";
import AvatarScene from "./components/AvatarScene.jsx";

const styles = {
  container: {
    minHeight: '95vh',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    padding: '20px',
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif"
  },
  
  mainCard: {
    width: '90vw',    
    minHeight: '100vh',
    margin: 0,
    backgroundColor: 'rgba(255, 255, 255, 0.95)',
    borderRadius: 10,
    padding: '30px',
    boxShadow: 'none',
    backdropFilter: 'blur(10px)'
  },

  header: {
    textAlign: 'center',
    marginBottom: '30px',
    color: '#2c3e50',
    fontSize: '2.5rem',
    fontWeight: '700',
    background: 'linear-gradient(45deg, #667eea, #764ba2)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text',
    textShadow: '0 2px 10px rgba(102, 126, 234, 0.3)'
  },
  
  controlsContainer: {
    backgroundColor: '#f8f9ff',
    borderRadius: '15px',
    padding: '25px',
    marginBottom: '25px',
    border: '1px solid #e1e8ff'
  },
  
  formGroup: {
    marginBottom: '20px'
  },
  
  label: {
    display: 'block',
    marginBottom: '8px',
    fontWeight: '600',
    color: '#4a5568',
    fontSize: '0.95rem'
  },
  
  select: {
    width: '100%',
    padding: '12px 16px',
    borderRadius: '10px',
    border: '2px solid #e1e8ff',
    fontSize: '1rem',
    backgroundColor: '#ffffff',
    color: '#2d3748',
    transition: 'all 0.3s ease',
    outline: 'none',
    cursor: 'pointer'
  },
  
  selectFocus: {
    borderColor: '#667eea',
    boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
  },
  
  radioGroup: {
    display: 'flex',
    gap: '20px',
    flexWrap: 'wrap',
    marginTop: '10px'
  },
  
  radioLabel: {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
    padding: '10px 16px',
    backgroundColor: '#ffffff',
    borderRadius: '10px',
    border: '2px solid #e1e8ff',
    transition: 'all 0.3s ease',
    fontWeight: '500',
    color: '#4a5568'
  },
  
  radioLabelChecked: {
    backgroundColor: '#667eea',
    borderColor: '#667eea',
    color: '#ffffff',
    transform: 'translateY(-2px)',
    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
  },
  
  radioLabelDisabled: {
    opacity: '0.5',
    cursor: 'not-allowed'
  },
  
  radioInput: {
    marginRight: '8px',
    accentColor: '#667eea'
  },
  
  fileInput: {
    width: '100%',
    padding: '16px',
    borderRadius: '10px',
    border: '2px dashed #667eea',
    backgroundColor: '#f8f9ff',
    textAlign: 'center',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    fontSize: '0.95rem',
    color: '#667eea'
  },
  
  fileInputHover: {
    backgroundColor: '#e1e8ff',
    borderColor: '#764ba2'
  },
  
  chatContainer: {
    border: '2px solid #e1e8ff',
    borderRadius: '15px',
    backgroundColor: '#ffffff',
    marginBottom: '20px',
    overflow: 'hidden',
    boxShadow: '0 4px 20px rgba(0, 0, 0, 0.05)'
  },
  
  chatHeader: {
    backgroundColor: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    padding: '15px 20px',
    fontWeight: '600',
    fontSize: '1.1rem',
    borderBottom: '1px solid #e1e8ff'
  },
  
  chatMessages: {
    height: '450px',
    overflowY: 'auto',
    padding: '15px',
    backgroundColor: '#fafbff'
  },
  
  messageContainer: {
    marginBottom: '15px',
    display: 'flex',
    flexDirection: 'column'
  },
  
  messageUser: {
    alignItems: 'flex-end'
  },
  
  messageBot: {
    alignItems: 'flex-start'
  },
  
  messageBubble: {
    maxWidth: '80%',
    padding: '12px 18px',
    borderRadius: '20px',
    fontSize: '0.95rem',
    lineHeight: '1.4',
    wordWrap: 'break-word'
  },
  
  messageBubbleUser: {
    backgroundColor: '#667eea',
    color: 'white',
    borderBottomRightRadius: '5px',
    marginLeft: 'auto',
    boxShadow: '0 3px 10px rgba(102, 126, 234, 0.3)'
  },
  
  messageBubbleBot: {
    backgroundColor: '#ffffff',
    color: '#2d3748',
    border: '1px solid #e1e8ff',
    borderBottomLeftRadius: '5px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)'
  },
  
  inputContainer: {
    display: 'flex',
    gap: '12px',
    alignItems: 'stretch'
  },
  
  textInput: {
    flex: 1,
    padding: '16px 20px',
    borderRadius: '25px',
    border: '2px solid #e1e8ff',
    fontSize: '1rem',
    color:'#000000',
    outline: 'none',
    transition: 'all 0.3s ease',
    backgroundColor: '#ffffff'
  },
  
  textInputFocus: {
    borderColor: '#667eea',
    boxShadow: '0 0 0 3px rgba(102, 126, 234, 0.1)'
  },
  
  voiceButton: {
    padding: '16px 20px',
    borderRadius: '25px',
    border: 'none',
    background: '#ffffff',
    color: '#667eea',
    fontWeight: '600',
    fontSize: '1.5rem',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    border: '2px solid #667eea',
    minWidth: '60px'
  },
  
  voiceButtonActive: {
    background: 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)',
    color: 'white',
    border: '2px solid #dc2626',
    animation: 'pulse 1.5s ease-in-out infinite'
  },
  
  sendButton: {
    padding: '16px 24px',
    borderRadius: '25px',
    border: 'none',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    color: 'white',
    fontWeight: '600',
    fontSize: '1rem',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 15px rgba(102, 126, 234, 0.3)',
    minWidth: '80px'
  },
  
  sendButtonHover: {
    transform: 'translateY(-2px)',
    boxShadow: '0 6px 20px rgba(102, 126, 234, 0.4)'
  },
  
  sendButtonDisabled: {
    opacity: '0.6',
    cursor: 'not-allowed',
    transform: 'none',
    boxShadow: '0 2px 8px rgba(102, 126, 234, 0.2)'
  },
  
  emptyChat: {
    textAlign: 'center',
    color: '#000000',
    fontSize: '1.1rem',
    marginTop: '50px',
    fontStyle: 'italic'
  },
  
  statusIndicator: {
    fontSize: '0.85rem',
    color: '#667eea',
    textAlign: 'center',
    marginTop: '8px',
    fontStyle: 'italic'
  }
};

export default function App() {
  const [grade, setGrade] = useState("");
  const [subject, setSubject] = useState("");
  const [medium, setMedium] = useState("english");
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [file, setFile] = useState(null);
  const [isHoveringFile, setIsHoveringFile] = useState(false);
  const [inputFocused, setInputFocused] = useState(false);
  const [selectFocused, setSelectFocused] = useState(false);
  const [isHoveringButton, setIsHoveringButton] = useState(false);
  const [language, setLanguage] = useState("en-IN");
  const [isListening, setIsListening] = useState(false);
  const [statusMessage, setStatusMessage] = useState("");
  const [selectedAvatar, setSelectedAvatar] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const [showAvatarSelection, setShowAvatarSelection] = useState(true);
  const recognitionRef = useRef(null);
  const synthesisRef = useRef(null);

  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.continuous = false;
      recognitionRef.current.interimResults = false;
      
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setInput(transcript);
        setStatusMessage("");
      };

      recognitionRef.current.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        setIsListening(false);
        setStatusMessage(`Error: ${event.error}`);
      };

      recognitionRef.current.onend = () => {
        setIsListening(false);
      };
    }

    if ('speechSynthesis' in window) {
      synthesisRef.current = window.speechSynthesis;
    }

    return () => {
      if (recognitionRef.current) {
        recognitionRef.current.stop();
      }
      if (synthesisRef.current) {
        synthesisRef.current.cancel();
      }
    };
  }, []);

  useEffect(() => {
    if (medium === "gujarati") {
      setLanguage("gu-IN");
    } else {
      setLanguage("en-IN");
    }
  }, [medium]);

  const toggleListening = () => {
    if (!recognitionRef.current) {
      setStatusMessage("Speech recognition not supported in this browser");
      return;
    }

    if (isListening) {
      recognitionRef.current.stop();
      setIsListening(false);
      setStatusMessage("");
    } else {
      recognitionRef.current.lang = language;
      recognitionRef.current.start();
      setIsListening(true);
      setStatusMessage("Listening...");
    }
  };

  const speakText = (text) => {
    if (!synthesisRef.current) {
      console.error("Speech synthesis not supported");
      return;
    }

    synthesisRef.current.cancel();

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = language;
    utterance.rate = 0.9;
    utterance.pitch = selectedAvatar === 'female' ? 1.1 : 0.9;

    const voices = synthesisRef.current.getVoices();
    let selectedVoice = null;
    const langPrefix = language.split('-')[0];
    const languageVoices = voices.filter(v => v.lang.startsWith(langPrefix));
    
    if (selectedAvatar === 'female') {
      selectedVoice = languageVoices.find(v => 
        v.name.toLowerCase().includes('female') ||
        v.name.toLowerCase().includes('woman') ||
        v.name.toLowerCase().includes('samantha') ||
        v.name.toLowerCase().includes('zira') ||
        v.name.toLowerCase().includes('heera') ||
        v.name.toLowerCase().includes('nicky')
      );
    } else {
      selectedVoice = languageVoices.find(v => 
        v.name.toLowerCase().includes('male') ||
        v.name.toLowerCase().includes('man') ||
        v.name.toLowerCase().includes('david') ||
        v.name.toLowerCase().includes('rishi') ||
        v.name.toLowerCase().includes('prabhat')
      );
    }
    
    if (!selectedVoice && languageVoices.length > 0) {
      selectedVoice = languageVoices[0];
    }
    
    if (selectedVoice) {
      utterance.voice = selectedVoice;
    }

    setIsSpeaking(true);
    
    utterance.onstart = () => {
      setIsSpeaking(true);
    };
    
    utterance.onend = () => {
      setIsSpeaking(false);
    };
    
    utterance.onerror = () => {
      setIsSpeaking(false);
    };

    synthesisRef.current.speak(utterance);
  };

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const formData = new FormData();
    formData.append("message", input);
    formData.append("grade", grade);
    const subjectToSend = medium === "gujarati" ? `gujarati_${subject}` : subject;
    formData.append("subject", subjectToSend);
    if (file) formData.append("file", file);

    const userMessage = input;
    setInput("");

    try {
      const res = await fetch("http://127.0.0.1:8000/ask", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      setMessages(prev => [
        ...prev, 
        { role: "user", text: userMessage }, 
        { role: "bot", text: data.answer }
      ]);
      
      speakText(data.answer);
    } catch (error) {
      console.error("Error:", error);
      const errorMsg = medium === "gujarati" 
        ? "માફ કરશો, કોઈ ભૂલ થઈ. કૃપા કરીને ફરી પ્રયાસ કરો." 
        : "Sorry, I encountered an error. Please try again.";
      setMessages(prev => [
        ...prev, 
        { role: "user", text: userMessage }, 
        { role: "bot", text: errorMsg }
      ]);
      speakText(errorMsg);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const isFormValid = grade && subject && input.trim();

  const getAvailableSubjects = () => {
    if (!grade) return [];

    if (medium === "gujarati") {
      if (grade === "1" || grade === "2") {
        return ["Maths", "Gujarati"];
      } else if (grade === "3") {
        return ["EVS", "Maths", "Gujarati"];
      }
      return ["Maths", "Gujarati"];
    } else {
      if (grade === "3") {
        return ["English", "Maths", "EVS"];
      }
      return ["English", "Maths"];
    }
  };

  const availableSubjects = getAvailableSubjects();

  return (
    <div style={styles.container}>
      {showAvatarSelection && (
        <AvatarSelection 
          onAvatarSelect={(avatarId) => {
            setSelectedAvatar(avatarId);
            setShowAvatarSelection(false);
          }}
        />
      )}
      
      <div style={styles.mainCard}>
        <h1 style={styles.header}>
          AI Teacher Bot | એઆઈ શિક્ષક બોટ
        </h1>
        
        <div style={styles.controlsContainer}>
          <div style={styles.formGroup}>
            <label style={styles.label}>Select Your Grade / તમારો ધોરણ પસંદ કરો</label>
            <select 
              value={grade} 
              onChange={(e) => {
                setGrade(e.target.value);
                setSubject("");
              }}
              style={{
                ...styles.select,
                ...(selectFocused ? styles.selectFocus : {})
              }}
              onFocus={() => setSelectFocused(true)}
              onBlur={() => setSelectFocused(false)}
            >
              <option value="">Choose your grade level...</option>
              <option value="1">Grade 1 / ધોરણ 1</option>
              <option value="2">Grade 2 / ધોરણ 2</option>
              <option value="3">Grade 3 / ધોરણ 3</option>
            </select>
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Choose Medium / માધ્યમ પસંદ કરો</label>
            <div style={styles.radioGroup}>
              {[
                { value: "english", label: "English Medium" },
                { value: "gujarati", label: "ગુજરાતી માધ્યમ (Gujarati Medium)" }
              ].map((med) => (
                <label 
                  key={med.value} 
                  style={{
                    ...styles.radioLabel,
                    ...(medium === med.value ? styles.radioLabelChecked : {}),
                    ...(grade === "" ? styles.radioLabelDisabled : {})
                  }}
                >
                  <input
                    type="radio"
                    name="medium"
                    value={med.value}
                    checked={medium === med.value}
                    onChange={(e) => {
                      setMedium(e.target.value);
                      setSubject("");
                    }}
                    disabled={grade === ""}
                    style={styles.radioInput}
                  />
                  {med.label}
                </label>
              ))}
            </div>
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Choose Subject / વિષય પસંદ કરો</label>
            <div style={styles.radioGroup}>
              {availableSubjects.map((subj) => (
                <label 
                  key={subj} 
                  style={{
                    ...styles.radioLabel,
                    ...(subject === subj ? styles.radioLabelChecked : {})
                  }}
                >
                  <input
                    type="radio"
                    name="subject"
                    value={subj}
                    checked={subject === subj}
                    onChange={(e) => setSubject(e.target.value)}
                    style={styles.radioInput}
                  />
                  {subj === "EVS" ? "Environmental Studies" : 
                   subj === "Gujarati" ? "ગુજરાતી" : subj}
                </label>
              ))}
              {availableSubjects.length === 0 && (
                <div style={{ color: '#718096', fontStyle: 'italic' }}>
                  Please select grade and medium first
                </div>
              )}
            </div>
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Voice Language / અવાજની ભાષા</label>
            <div style={styles.radioGroup}>
              {[
                { code: "en-IN", name: "English" },
                { code: "hi-IN", name: "हिन्दी (Hindi)" },
                { code: "gu-IN", name: "ગુજરાતી (Gujarati)" }
              ].map((lang) => (
                <label 
                  key={lang.code} 
                  style={{
                    ...styles.radioLabel,
                    ...(language === lang.code ? styles.radioLabelChecked : {})
                  }}
                >
                  <input
                    type="radio"
                    name="language"
                    value={lang.code}
                    checked={language === lang.code}
                    onChange={(e) => setLanguage(e.target.value)}
                    style={styles.radioInput}
                  />
                  {lang.name}
                </label>
              ))}
            </div>
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Upload Learning Materials (Optional) / શીખવાની સામગ્રી અપલોડ કરો</label>
            <div
              style={{
                ...styles.fileInput,
                ...(isHoveringFile ? styles.fileInputHover : {})
              }}
              onMouseEnter={() => setIsHoveringFile(true)}
              onMouseLeave={() => setIsHoveringFile(false)}
            >
              <input 
                type="file" 
                onChange={(e) => setFile(e.target.files[0])}
                style={{ display: 'none' }}
                id="file-upload"
              />
              <label htmlFor="file-upload" style={{ cursor: 'pointer', display: 'block' }}>
                📎 {file ? file.name : 'Click to upload documents, images, or other materials'}
              </label>
            </div>
          </div>
        </div>

        <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
          {selectedAvatar && (
            <AvatarScene 
              gender={selectedAvatar} 
              isSpeaking={isSpeaking}
            />
          )}
          
          <div style={{ ...styles.chatContainer, flex: 1 }}>
            <div style={styles.chatHeader}>
              💬 Chat with your AI Teacher / તમારા એઆઈ શિક્ષક સાથે ચેટ કરો
            </div>
            
            <div style={styles.chatMessages}>
              {messages.length === 0 ? (
                <div style={styles.emptyChat}>
                  {medium === "gujarati" 
                    ? "👋 નમસ્તે! હું તમારો એઆઈ શિક્ષક છું. ઉપર તમારો ધોરણ અને વિષય પસંદ કરો, પછી મને કંઈપણ પૂછો!"
                    : "👋 Hello! I'm your AI teacher. Select your grade and subject above, then ask me anything!"}
                </div>
              ) : (
                messages.map((m, i) => (
                  <div 
                    key={i} 
                    style={{
                      ...styles.messageContainer,
                      ...(m.role === "user" ? styles.messageUser : styles.messageBot)
                    }}
                  >
                    <div
                      style={{
                        ...styles.messageBubble,
                        ...(m.role === "user" ? styles.messageBubbleUser : styles.messageBubbleBot)
                      }}
                    >
                      {m.text}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        <div style={styles.inputContainer}>
          <button
            onClick={toggleListening}
            style={{
              ...styles.voiceButton,
              ...(isListening ? styles.voiceButtonActive : {})
            }}
            title={isListening ? "Stop listening" : "Start voice input"}
          >
            {isListening ? "🔴" : "🎤"}
          </button>
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder={medium === "gujarati" 
              ? "તમારો પ્રશ્ન અહીં લખો અથવા અવાજનો ઉપયોગ કરો..."
              : "Type your question here or use voice input..."}
            style={{
              ...styles.textInput,
              ...(inputFocused ? styles.textInputFocus : {})
            }}
            onFocus={() => setInputFocused(true)}
            onBlur={() => setInputFocused(false)}
          />
          <button 
            onClick={handleSend}
            disabled={!isFormValid}
            style={{
              ...styles.sendButton,
              ...(isHoveringButton && isFormValid ? styles.sendButtonHover : {}),
              ...(!isFormValid ? styles.sendButtonDisabled : {})
            }}
            onMouseEnter={() => setIsHoveringButton(true)}
            onMouseLeave={() => setIsHoveringButton(false)}
          >
            {medium === "gujarati" ? "મોકલો" : "Send"}
          </button>
        </div>
        {statusMessage && (
          <div style={styles.statusIndicator}>{statusMessage}</div>
        )}
      </div>
      <style>{`
        @keyframes pulse {
          0%, 100% {
            transform: scale(1);
          }
          50% {
            transform: scale(1.05);
          }
        }
      `}</style>
    </div>
  );
}