y9; /**
 * Discord Notification Utility for Frontend (Vite/Vue/React)
 *
 * Note: Direct calls to Discord Webhook from frontend may expose the Webhook URL if not proxied.
 * RECOMMENDED: Use a backend proxy to hide the Webhook URL.
 * If you must use it directly (e.g. internal tools), ensure the URL is not public.
 */

const WEBHOOK_URL = import.meta.env.VITE_DISCORD_WEBHOOK_URL;

export const sendNotification = async (message, level = 'info') => {
	if (!WEBHOOK_URL) {
		console.warn('VITE_DISCORD_WEBHOOK_URL is not set');
		return;
	}

	const payload = {
		embeds: [
			{
				title: level === 'error' ? '🚨 前端錯誤' : 'ℹ️ 通知',
				description: message.substring(0, 4000),
				color: level === 'error' ? 0xff0000 : 0x3498db,
				timestamp: new Date().toISOString(),
			},
		],
	};

	try {
		await fetch(WEBHOOK_URL, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(payload),
		});
	} catch (error) {
		console.error('Failed to send notification', error);
	}
};

export const useNotification = () => {
	return {
		notify: sendNotification,
		notifyError: (error, context = '') => {
			const msg = context
				? `${context}: ${error.message}`
				: error.message;
			sendNotification(msg, 'error');
		},
	};
};
