"use client";
import { useState, useEffect } from "react";
import { createClient, User, Session } from "@supabase/supabase-js";

const supabase = createClient(
    process.env.NEXT_PUBLIC_SUPABASE_URL!,
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!
);

export function useSupabaseAuth() {
    const [user, setUser] = useState<User | null>(null);
    const [session, setSession] = useState<Session | null>(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchSession = async () => {
            const {
                data: { session },
                error,
            } = await supabase.auth.getSession();
            if (error) {
                setError(error.message);
            } else if (session) {
                setUser(session.user);
                setSession(session);
            }
            setLoading(false);
        };

        fetchSession();

        const { data: authListener } = supabase.auth.onAuthStateChange(
            async (event, session) => {
                setUser(session?.user ?? null);
                setSession(session);
                setLoading(false);
            }
        );

        return () => {
            authListener.subscription.unsubscribe();
        };
    }, []);

    const signIn = async (email: string, password: string) => {
        setLoading(true);
        setError(null);
        try {
            const { data, error } = await supabase.auth.signInWithPassword({
                email,
                password,
            });
            if (error) throw error;
            return data.user;
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "An error occurred during sign in"
            );
        } finally {
            setLoading(false);
        }
    };

    const signInWithGoogle = async () => {
        setLoading(true);
        setError(null);
        try {
            const { data, error } = await supabase.auth.signInWithOAuth({
                provider: "google",
            });
            if (error) throw error;
            return data;
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "An error occurred during Google sign in"
            );
        } finally {
            setLoading(false);
        }
    };

    const signOut = async () => {
        setLoading(true);
        try {
            const { error } = await supabase.auth.signOut();
            if (error) throw error;
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "An error occurred during sign out"
            );
        } finally {
            setLoading(false);
        }
    };

    const signUp = async (email: string, password: string) => {
        setLoading(true);
        setError(null);
        try {
            const { data, error } = await supabase.auth.signUp({
                email,
                password,
            });
            if (error) throw error;
            return data;
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "An error occurred during sign up"
            );
        } finally {
            setLoading(false);
        }
    };

    const signUpWithGoogle = async () => {
        setLoading(true);
        setError(null);
        try {
            const { data, error } = await supabase.auth.signInWithOAuth({
                provider: "google",
                options: {
                    scopes: "email profile",
                },
            });
            if (error) throw error;
            if (!data) {
                throw new Error("User not found");
            }
            return data;
        } catch (err) {
            setError(
                err instanceof Error
                    ? err.message
                    : "An error occurred during sign up with Google"
            );
        } finally {
            setLoading(false);
        }
    };

    return {
        user,
        session,
        loading,
        error,
        signIn,
        signInWithGoogle,
        signOut,
        signUp,
        signUpWithGoogle,
    };
}
