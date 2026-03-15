export function toISOString(date: Date): string {
  return date.toISOString();
}

export function generateId(): string {
  return crypto.randomUUID();
}
