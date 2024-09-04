"use client";
import React, { useEffect, useState, useCallback } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useItineraryApi } from "@/hooks/useItineraryApi";

interface Itinerary {
    id: string;
    title: string;
    start_date: string;
    end_date: string;
    total_budget: number;
}

export function ItineraryList() {
    const [itineraries, setItineraries] = useState<Itinerary[]>([]);
    const {
        generateItinerary,
        getItineraries,
        deleteItinerary,
        loading,
        error,
    } = useItineraryApi();

    const fetchItineraries = useCallback(async () => {
        const data = await getItineraries();
        if (data) setItineraries(data);
    }, [getItineraries, setItineraries]);

    useEffect(() => {
        fetchItineraries();
    }, [fetchItineraries]);

    const handleDelete = async (id: string) => {
        await deleteItinerary(id);
        fetchItineraries();
    };

    if (loading) return <p>Loading itineraries...</p>;
    if (error) return <p className="text-red-500">{error}</p>;

    return (
        <div className="space-y-4">
            <h2 className="text-2xl font-bold">Your Itineraries</h2>
            {itineraries.map((itinerary) => (
                <Card key={itinerary.id}>
                    <CardHeader>
                        <CardTitle>{itinerary.title}</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <p>
                            Start Date:{" "}
                            {new Date(
                                itinerary.start_date
                            ).toLocaleDateString()}
                        </p>
                        <p>
                            End Date:{" "}
                            {new Date(itinerary.end_date).toLocaleDateString()}
                        </p>
                        <p>Total Budget: ${itinerary.total_budget}</p>
                        <div className="mt-4 space-x-2">
                            <Button
                                onClick={() => {
                                    /* Navigate to itinerary details */
                                }}>
                                View Details
                            </Button>
                            <Button
                                variant="destructive"
                                onClick={() => handleDelete(itinerary.id)}>
                                Delete
                            </Button>
                        </div>
                    </CardContent>
                </Card>
            ))}
        </div>
    );
}
