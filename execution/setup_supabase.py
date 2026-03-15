import os

def setup_supabase():
    # 1. SQL migration file
    migration_path = "execution/migrations/001_waitlist.sql"
    os.makedirs(os.path.dirname(migration_path), exist_ok=True)
    
    sql_content = """-- Waitlist Setup
CREATE TABLE IF NOT EXISTS waitlist (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users ON DELETE CASCADE,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    position SERIAL,
    joined_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    provider TEXT
);

-- Enable RLS
ALTER TABLE waitlist ENABLE ROW LEVEL SECURITY;

-- RLS Policies
CREATE POLICY "Users can view their own waitlist entry" ON waitlist
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own waitlist entry" ON waitlist
    FOR INSERT WITH CHECK (auth.uid() = user_id);
    
-- Realtime for waitlist count
ALTER PUBLICATION supabase_realtime ADD TABLE waitlist;
"""
    with open(migration_path, "w") as f:
        f.write(sql_content)
    print(f"Created migration: {migration_path}")

    # 2. Supabase client
    client_path = "frontend/src/lib/supabase.ts"
    os.makedirs(os.path.dirname(client_path), exist_ok=True)
    
    client_content = """import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseAnonKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export const supabase = createClient(supabaseUrl, supabaseAnonKey);
"""
    with open(client_path, "w") as f:
        f.write(client_content)
    print(f"Created Supabase client: {client_path}")

    # 3. .env.example cleanup/update
    env_example_path = ".env.example"
    with open(env_example_path, "w") as f:
        f.write("# Supabase Configuration\n")
        f.write("NEXT_PUBLIC_SUPABASE_URL=\n")
        f.write("NEXT_PUBLIC_SUPABASE_ANON_KEY=\n")
        f.write("NEXT_PUBLIC_SITE_URL=http://localhost:3000\n")
    print(f"Reset and updated: {env_example_path}")

if __name__ == "__main__":
    setup_supabase()
