import React, { useState } from "react";
import { useSupabaseAuth } from "@/hooks/useSupabaseAuth";
import DOMPurify from "dompurify";
import Register from "./Register";

interface LoginProps {
    onLogin: (user: any) => void;
}

const Login: React.FC<LoginProps> = ({ onLogin }) => {
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
    const [passwordError, setPasswordError] = useState("");
    const [isRegistering, setIsRegistering] = useState(false);

    const handleGoogleLogin = async () => {
        try {
            await signInWithGoogle();
            onLogin(user);
        } catch (error) {
            console.error(error);
        }
    };

    const handleCredentialLogin = async () => {
        try {
            // Sanitize inputs using PurifyDOM
            const sanitizedEmail = DOMPurify.sanitize(email);
            const sanitizedPassword = DOMPurify.sanitize(password);

            await signIn(sanitizedEmail, sanitizedPassword);
            onLogin(user);
        } catch (error) {
            console.error(error);
        }
    };

    const handleToggleRegister = () => {
        setIsRegistering(!isRegistering);
    };

    return (
        <div>
            {isRegistering ? (
                <Register onRegister={onLogin} />
            ) : (
                <div>
                    <h2>Login</h2>
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
                        <button onClick={handleCredentialLogin}>Login</button>
                        <button onClick={handleGoogleLogin}>
                            Login with Google
                        </button>
                    </form>
                    <p>
                        Don&apos;t have an account?{" "}
                        <button onClick={handleToggleRegister}>Register</button>
                    </p>
                </div>
            )}
        </div>
    );
};

export default Login;
