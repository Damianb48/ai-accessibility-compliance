import type { NextApiRequest, NextApiResponse } from 'next';

// This is a placeholder webhook handler. In production you must
// verify the Stripe signature and update your Supabase `subscriptions`
// table accordingly.
export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    // TODO: verify signature using stripe.webhooks.constructEvent
    console.log('Received Stripe webhook:', req.body);
    return res.status(200).json({ received: true });
  }
  res.setHeader('Allow', 'POST');
  res.status(405).end('Method Not Allowed');
}
