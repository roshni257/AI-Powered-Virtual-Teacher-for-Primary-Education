import { Avatar_Male } from './Avatar_Male';
import { Avatar_Female } from './Avatar_Female';

export default function TeacherAvatar({ gender, isSpeaking, ...props }) {
    const AvatarComponent = gender === 'female' ? Avatar_Female : Avatar_Male;
    return <AvatarComponent isSpeaking={isSpeaking} {...props} />;
}
