"use client";
import React, { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { useItineraryApi } from "@/hooks/useItineraryApi";

export function ItineraryForm() {
    const [preferences, setPreferences] = useState({
        budget: "",
        duration: "",
        interests: "",
        destinations: "",
    });
    const { generateItinerary, loading, error } = useItineraryApi();

    const cleanInput = (input: string) => {
        return input.trim().replace(/[<>]/g, "");
    };

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const { name, value } = e.target;
        setPreferences((prev) => ({ ...prev, [name]: cleanInput(value) }));
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        const userPreferences = {
            interests: preferences.interests
                .split(",")
                .map((i) => cleanInput(i)),
            budget: Number(preferences.budget),
            preferred_travel_style: "balanced",
            preferred_activities: [],
        };
        const destinations = preferences.destinations
            .split(",")
            .map((d) => cleanInput(d));
        await generateItinerary(
            userPreferences,
            destinations,
            Number(preferences.duration)
        );
    };

    return (
        <Card>
            <CardHeader>
                <CardTitle>Create New Itinerary</CardTitle>
            </CardHeader>
            <CardContent>
                <form
                    onSubmit={handleSubmit}
                    className="space-y-4">
                    <div>
                        <Label htmlFor="budget">Budget</Label>
                        <Input
                            id="budget"
                            name="budget"
                            type="number"
                            placeholder="Enter your budget"
                            value={preferences.budget}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    <div>
                        <Label htmlFor="duration">Duration (days)</Label>
                        <Input
                            id="duration"
                            name="duration"
                            type="number"
                            placeholder="Enter trip duration"
                            value={preferences.duration}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    <div>
                        <Label htmlFor="interests">Interests</Label>
                        <Input
                            id="interests"
                            name="interests"
                            placeholder="e.g., history, nature, food"
                            value={preferences.interests}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    <div>
                        <Label htmlFor="destinations">Destinations</Label>
                        <Input
                            id="destinations"
                            name="destinations"
                            placeholder="e.g., Paris, Rome, Barcelona"
                            value={preferences.destinations}
                            onChange={handleInputChange}
                            required
                        />
                    </div>
                    {error && <p className="text-red-500">{error}</p>}
                    <Button
                        type="submit"
                        disabled={loading}>
                        {loading ? "Generating..." : "Generate Itinerary"}
                    </Button>
                </form>
            </CardContent>
        </Card>
    );
}
