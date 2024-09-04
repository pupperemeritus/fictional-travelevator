import React, { useState } from "react";
import { useSupabaseAuth } from "@/hooks/useSupabaseAuth";
import DOMPurify from "dompurify";

interface RegisterProps {
    onRegister: (user: any) => void;
}

const Register: React.FC<RegisterProps> = ({ onRegister }) => {
    const {
        user,
        loading,
        error,
        signIn,
        signInWithGoogle,
        signOut,
        signUp,
        signUpWithGoogle,
    } = useSupabaseAuth();
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [fullName, setFullName] = useState("");

    const handleRegister = async () => {
        try {
            // Sanitize inputs using PurifyDOM
            const sanitizedEmail = DOMPurify.sanitize(email);
            const sanitizedPassword = DOMPurify.sanitize(password);
            const sanitizedFullName = DOMPurify.sanitize(fullName);

            await signUp(sanitizedEmail, sanitizedPassword);

            onRegister(user);
        } catch (error) {
            console.error(error);
        }
    };

    const handleGoogleRegister = async () => {
        try {
            await signUpWithGoogle();
            onRegister(user);
        } catch (error) {
            console.error(error);
        }
    };

    return (
        <div>
            <h2>Register</h2>
            <form>
                <input
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="Email"
                />
                <input
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="Password"
                />
                <input
                    type="text"
                    value={fullName}
                    onChange={(e) => setFullName(e.target.value)}
                    placeholder="Full Name"
                />
                <button
                    type="button"
                    onClick={handleGoogleRegister}>
                    Register with Google
                </button>
                <button
                    type="button"
                    onClick={handleRegister}>
                    Register
                </button>
            </form>
        </div>
    );
};

export default Register;
