"use client";
import { useState } from "react";
import { useSupabaseAuth } from "./useSupabaseAuth";

interface UserPreferences {
    interests: string[];
    budget: number;
    preferred_travel_style: string;
    preferred_activities: string[];
    accessibility_needs?: string[];
}

interface Destination {
    destination_id: string;
    arrival_time: string;
    departure_time: string;
    travel_time_from_previous?: number;
    travel_cost_from_previous?: number;
}

interface Itinerary {
    title: string;
    start_date: string;
    end_date: string;
    user_id: string;
    total_budget: number;
    destinations: Destination[];
    id: string;
    created_at: string;
    updated_at: string;
}

export function useItineraryApi() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const { user } = useSupabaseAuth();

    const headers = {
        "Content-Type": "application/json",
        "user-id": user?.id || "",
    };

    const generateItinerary = async (
        userPreferences: UserPreferences,
        destinations: string[],
        duration: number
    ): Promise<Itinerary | null> => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch("/itineraries/generate", {
                method: "POST",
                headers,
                body: JSON.stringify({
                    user_preferences: userPreferences,
                    destinations,
                    duration,
                }),
            });

            if (!response.ok) {
                throw new Error("Failed to generate itinerary");
            }

            const data: Itinerary = await response.json();
            return data;
        } catch (err) {
            setError(
                err instanceof Error ? err.message : "An unknown error occurred"
            );
            return null;
        } finally {
            setLoading(false);
        }
    };

    const getItineraries = async (): Promise<Itinerary[] | null> => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch("/itineraries", {
                method: "GET",
                headers,
            });

            if (!response.ok) {
                throw new Error("Failed to fetch itineraries");
            }

            const data: Itinerary[] = await response.json();
            return data;
        } catch (err) {
            setError(
                err instanceof Error ? err.message : "An unknown error occurred"
            );
            return null;
        } finally {
            setLoading(false);
        }
    };

    const deleteItinerary = async (id: string): Promise<void> => {
        setLoading(true);
        setError(null);

        try {
            const response = await fetch(`/itineraries/${id}`, {
                method: "DELETE",
                headers,
            });

            if (!response.ok) {
                throw new Error("Failed to delete itinerary");
            }
        } catch (err) {
            setError(
                err instanceof Error ? err.message : "An unknown error occurred"
            );
        } finally {
            setLoading(false);
        }
    };

    return {
        generateItinerary,
        getItineraries,
        deleteItinerary,
        loading,
        error,
    };
}
