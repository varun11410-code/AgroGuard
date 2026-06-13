export interface ValidationResult {
  isValid: boolean;
  errors: string[];
}

export const MAX_FILE_SIZE_MB = 10;
export const MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024;
export const ALLOWED_MIME_TYPES = [
  "image/jpeg",
  "image/png",
  "image/jpg",
  "image/webp"
];

export function validateImageFile(file: File | null | undefined): ValidationResult {
  const errors: string[] = [];

  if (!file) {
    errors.push("No file provided.");
    return { isValid: false, errors };
  }

  if (file.size === 0) {
    errors.push("File is empty.");
  }

  if (file.size > MAX_FILE_SIZE_BYTES) {
    errors.push(`File exceeds the maximum allowed size of ${MAX_FILE_SIZE_MB}MB.`);
  }

  if (!ALLOWED_MIME_TYPES.includes(file.type)) {
    errors.push("Invalid file type. Only JPG, PNG, and WEBP images are allowed.");
  }

  return {
    isValid: errors.length === 0,
    errors,
  };
}
