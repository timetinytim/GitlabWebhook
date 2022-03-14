import { checkVideoFiles, expandFiles } from '../lib/filesystem.js';

/**
 * Encode the files provided by the user.
 *
 * By default, will analyze each video file provided, then encode them.
 * Depending on the provided flags, might also expand out directories, or skip
 * the encodin step.
 *
 * @param {Array<string>} files List of files (and/or directories) to encode.
 * @param {object} options CLI options.
 */
export function encode(files, options) {
	// Expand out files if asked to do so.
	files = expandFiles(files);

	// Check files to make sure they are valid.
	files = checkVideoFiles(files, options.recursive);
}
