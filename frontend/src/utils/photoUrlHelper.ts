// utils/photoUrlHelper.ts
export function buildPhotoUrl(
    photoPath: string | null | undefined, 
    bucketName: string = 'ssis_web_bucket'
): string {
    if (!photoPath) {
        console.log('No photo path provided, returning empty string.');
        return "";
    }
    
    try {
        const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || "https://oqqrwmdagqrtkqbfxnlt.supabase.co";
        
        const cleanPath = photoPath.startsWith('/') ? photoPath.slice(1) : photoPath;

        let finalPath: string;
        if (cleanPath.startsWith(`${bucketName}/`)) {
            finalPath = cleanPath;
        } else {
            finalPath = `${bucketName}/${cleanPath}`;
        }

        const url = `${supabaseUrl}/storage/v1/object/public/${finalPath}`;
        console.log('Built photo URL:', url);
        
        return url;
    } catch (error) {
        console.error('Error building photo URL:', error);
        return "";
    }
}

// Helper to check if URL is valid
export function isValidPhotoUrl(url: string | null): boolean {
    return !!url && (url.startsWith('http://') || url.startsWith('https://'));
}