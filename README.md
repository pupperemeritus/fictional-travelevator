# fictional-travelevator

## The backend and data design

I have chosen FastAPI to build my backend. The reason is twofold, I have a lot of familiarity with the python ecosystem of libraries and it allows me to integrate locally running AI/ML much easier than say typescript.

### How do I tackle this without using paid APIs?

I have decided to scrape data from wikipedia at the list of towns and cities to get a general description, location, geography, famous places and other information. I then store this data in a ChromaDB Vector Store. I use Llama3.1:8b to locally populate my destinations with assistance from the data store. This will ensure that my data mock is somewhat accurate to real life. I am going to use pydantic to verify that the LLM's output is in the specified format both in terms of schema and datatypes.

### The backend services

I am creating services for the following so that I can use them across my backend quite effortlessly.

- LLM
- Supabase
- Vector Store

### The backend Routes

I am going to add a middleware to all my routes so they are authenticated.

I currently have the following routes

- /users/me
- /itineraries/
- /itineraries/{id}
- /itineraries/generate
- /destinations
- /destinations/{id}

### Data Models

I am using Supabase as my database. Reason for choosing Supabase is that it provides Row Level Security and easy authentication across all authentication providers and provides great integration with frontends. Since I am not dealing with data thats too large or unstructured, the Postgres DB should serve me fine. As usual I am using pydantic to validate my data.

The following is the current data model. It is bound to change with time. For now this is the state

Place

- name
- type (city, state, country)
- parent_id
- latitude
- longitude

User Preferences

- interests
- budget
- preferred-travel-style
- preferred-activities
- accessibility-needs

Activity

- name
- description
- start_time
- end_time
- cost
- tags
- place_id

Itinerary

- title
- start_date
- end_date
- user_id
- total_budget
- destinations

Destination in Itinerary

- destination_id
- arrival_time
- departure_time
- travel_time_from_previous
- travel_cost_from_previous

User

User IDs and authentication taken care of by Supabase. Taken care of by supabase

## The frontend

I have decided to use Next.js with Typescript, Tailwind CSS and shadcn/ui to provide some well styled base components. As I mentioned earlier I am using supabase for auth. Since my fronend finesse is quite limited I have decided to keep it barebones for now. Just plan to use Supabase and my backend to display and generate itineraries specific to user preferences.
