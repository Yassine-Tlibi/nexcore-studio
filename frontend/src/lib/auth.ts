import { supabase } from './supabase';

export const signUpWithEmail = async (email: string, password: string, fullName: string) => {
  const { data, error } = await supabase.auth.signUp({
    email,
    password,
    options: {
      data: { full_name: fullName },
    }
  });
  if (error) throw error;

  // Add to waitlist
  if (data.user) {
    const { data: waitlist, error: waitlistError } = await supabase
      .from('waitlist')
      .insert({
        user_id: data.user.id,
        email: email,
        full_name: fullName,
      })
      .select()
      .single();
    
    if (waitlistError) throw waitlistError;
    return waitlist;
  }
};

export const signInWithEmail = async (email: string, password: string) => {
  const { error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) throw error;
};

export const getCurrentUser = async () => {
  const { data: { user } } = await supabase.auth.getUser();
  return user;
};

export const signOut = async () => {
  return await supabase.auth.signOut();
};
