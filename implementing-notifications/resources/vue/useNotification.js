/**
 * Notification Composable for Vue 3 (Works with Vite and Webpack)
 */

// Try to get env from import.meta (Vite) or process.env (Webpack/Jest)
const getEnv = (key) => {
	try {
		// @ts-ignore
		if (typeof import.meta !== 'undefined' && import.meta.env) {
			// @ts-ignore
			return import.meta.env[key] || import.meta.env[`VITE_${key}`];
		}
	} catch (e) {}

	try {
		// @ts-ignore
		if (typeof process !== 'undefined' && process.env) {
			// @ts-ignore
			return process.env[key] || process.env[`VUE_APP_${key}`];
		}
	} catch (e) {}

	return '';
};

const WEBHOOK_URL = getEnv('DISCORD_WEBHOOK_URL');

export const useNotification = () => {
	const notify = async (message, level = 'info') => {
		if (!WEBHOOK_URL) {
			console.warn(
				'Discord Webhook URL not found (checked VITE_DISCORD_WEBHOOK_URL and VUE_APP_DISCORD_WEBHOOK_URL)',
			);
			return;
		}

		const colors = {
			info: 0x3498db,
			error: 0xff0000,
			warning: 0xffa500,
		};

		const payload = {
			embeds: [
				{
					title:
						level === 'error'
							? '🚨 Application Error'
							: 'ℹ️ Notification',
					description: message.substring(0, 4000),
					color: colors[level] || colors.info,
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

	const notifyError = (error, context = '') => {
		const msg = context
			? `${context}: ${error.message || error}`
			: error.message || error;
		notify(msg, 'error');
	};

	return {
		notify,
		notifyError,
	};
};
