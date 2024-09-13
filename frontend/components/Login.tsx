import { useSupabaseAuth } from "@/hooks/useSupabaseAuth";
import DOMPurify from "dompurify";
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
    Card,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card";
import { User } from "@supabase/supabase-js";
import { Label } from "@/components/ui/label";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { FaGoogle } from "react-icons/fa";
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
        <div className="flex items-center justify-center min-h-screen bg-gray-100">
            <Card className="w-[350px]">
                <CardHeader>
                    <CardTitle>Welcome</CardTitle>
                    <CardDescription>
                        Sign in to your account or create a new one.
                    </CardDescription>
                </CardHeader>
                <CardContent>
                    <Tabs
                        defaultValue="login"
                        className="w-full">
                        <TabsList className="grid w-full grid-cols-2">
                            <TabsTrigger value="login">Login</TabsTrigger>
                            <TabsTrigger value="register">Register</TabsTrigger>
                        </TabsList>
                        <TabsContent value="login">
                            <form
                                onSubmit={handleCredentialLogin}
                                className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="email">Email</Label>
                                    <Input
                                        id="email"
                                        type="email"
                                        value={email}
                                        onChange={(e) =>
                                            setEmail(e.target.value)
                                        }
                                        placeholder="Enter your email"
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="password">Password</Label>
                                    <Input
                                        id="password"
                                        type="password"
                                        value={password}
                                        onChange={(e) =>
                                            setPassword(e.target.value)
                                        }
                                        placeholder="Enter your password"
                                        required
                                    />
                                </div>
                                <Button
                                    type="submit"
                                    className="w-full">
                                    Login
                                </Button>
                            </form>
                        </TabsContent>
                        <TabsContent value="register">
                            <form
                                onSubmit={handleCredentialLogin}
                                className="space-y-4">
                                <div className="space-y-2">
                                    <Label htmlFor="register-email">
                                        Email
                                    </Label>
                                    <Input
                                        id="register-email"
                                        type="email"
                                        placeholder="Enter your email"
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="register-password">
                                        Password
                                    </Label>
                                    <Input
                                        id="register-password"
                                        type="password"
                                        placeholder="Create a password"
                                        required
                                    />
                                </div>
                                <div className="space-y-2">
                                    <Label htmlFor="confirm-password">
                                        Confirm Password
                                    </Label>
                                    <Input
                                        id="confirm-password"
                                        type="password"
                                        placeholder="Confirm your password"
                                        required
                                    />
                                </div>
                                <Button
                                    type="submit"
                                    className="w-full">
                                    Register
                                </Button>
                            </form>
                        </TabsContent>
                    </Tabs>
                </CardContent>
                <CardFooter>
                    <Button
                        onClick={handleGoogleLogin}
                        variant="outline"
                        className="w-full">
                        <FaGoogle className="mr-2" />
                        Login with Google
                    </Button>
                </CardFooter>
            </Card>
        </div>
    );
};

export default Login;
