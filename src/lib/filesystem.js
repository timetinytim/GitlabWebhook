import chalk from 'chalk';
import fs from 'fs';
import path from 'path';

import { config } from '../config.js';

/**
 * Functions for interacting with the filesystem.
 */

/**
 * Expands any directories in a given list of video files to encode.
 *
 * For any directories found in the provided list of files, they are
 * replaced with a list of files found inside that directory.
 *
 * @param {Array<string>} files List of files (and possibly directories).
 * @param {number} depth How far down into recursion we've gone.
 * @returns {Array<string>} List of expanded video files..
 */
export function expandFiles (files, depth = 0) {
	let newList = [];

	files.forEach((file) => {

		// Ignore if we can't find it
		if (! fs.existsSync(file)) {
			newList.push(file);
			return;
		}

		// If it's a directory, check subdirectories.
		if (
			fs.lstatSync(file).isDirectory() &&
			depth < config.recursionDepth
		) {
			const children = fs.readdirSync(file);
			children.forEach((child) => {
				const childPath = path.join(file, child);
				if (fs.lstatSync(childPath).isDirectory()) {
					newList.concat(expandFiles([childPath], ++depth));
				} else {
					newList.push(childPath);
				}
			});
		} else {
			newList.push(file);
		}
	});

	return newList;
}

/**
 * Checks the given list of filepaths to make sure they are supported filetypes,
 * and returns a list of valid files.
 *
 * If there are any invalid files, they are removed from the returned list.
 * This includes directories when not including --recursive.
 *
 * @param {Array<string>} files List of filepaths to check.
 * @param {boolean} recursive Whether or not we are looking at subdirs.
 * @returns {Array<string>} List of valid files.
 */
export function checkVideoFiles (files, recursive) {
	let validFiles = [];

	files.forEach((file) => {

		// Does the file exist?
		if (! fs.existsSync(file)) {
			console.log(chalk.yellowBright(
				`WARNING: '${file}' not found. Skipping...`
			));
			return;
		}


		// If we have a directory, are we recursing?
		if (fs.lstatSync(file).isDirectory() && ! recursive) {
			console.log(chalk.yellowBright(
				`WARNING: '${file}' is a directory. Skipping...`
			));
			return;
		}


		// Is the file a supported type?
		if (
			! fs.lstatSync(file).isDirectory() &&
			config.supportedFiles.indexOf(path.extname(file)) < 0
		) {
			console.log(chalk.yellowBright(
				`WARNING: '${file}': unsupported file format. Skipping...`
			));
			return;
		}

		validFiles.push(file);
	});

	return validFiles;
}
