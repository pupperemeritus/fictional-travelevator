"use client";
import React, { useState, useEffect } from "react";
import { ItineraryList } from "@/components/ItineraryList";
import { ItineraryForm } from "@/components/ItineraryForm";
import { useSupabaseAuth } from "@/hooks/useSupabaseAuth";
import Login from "@/components/Login";

export default function Home() {
    const {
        user: authUser,
        loading,
        error,
        signIn,
        signInWithGoogle,
        signOut,
        signUp,
        signUpWithGoogle,
    } = useSupabaseAuth();

    const [user, setUser] = useState(authUser);

    useEffect(() => {
        if (authUser) {
            setUser(authUser);
        }
    }, [authUser]);

    const handleLogin = (loggedInUser: any) => {
        // Update user state when the user logs in
        setUser(loggedInUser);
    };

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    if (!user) {
        return <Login onLogin={handleLogin} />; // Render Login component when not logged in
    }

    return (
        <div className="container mx-auto p-4">
            <header className="flex justify-between items-center mb-8">
                <h1 className="text-4xl font-bold">Travel Itinerary Planner</h1>
                <button
                    onClick={signOut}
                    className="text-blue-500 hover:underline">
                    Logout
                </button>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                <div>
                    <h2 className="text-2xl font-semibold mb-4">
                        Create New Itinerary
                    </h2>
                    <ItineraryForm />
                </div>
                <div>
                    <ItineraryList />
                </div>
            </div>
        </div>
    );
}
