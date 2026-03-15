import { createRouteHandlerClient } from '@supabase/auth-helpers-nextjs';
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const requestUrl = new URL(request.url);
  const code = requestUrl.searchParams.get('code');

  if (code) {
    const supabase = createRouteHandlerClient({ cookies });
    const { data: { user } } = await supabase.auth.exchangeCodeForSession(code);
    
    if (user) {
      // Check if in waitlist
      const { data: existing } = await supabase
        .from('waitlist')
        .select('id')
        .eq('user_id', user.id)
        .single();
      
      if (!existing) {
        await supabase.from('waitlist').insert({
          user_id: user.id,
          email: user.email!,
          full_name: user.user_metadata.full_name,
          provider: 'google'
        });
      }
    }
  }

  return NextResponse.redirect(`${requestUrl.origin}/waitlist/success`);
}
