-- Waitlist Setup
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
