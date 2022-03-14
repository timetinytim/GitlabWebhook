import { program } from 'commander';

import { encode } from './src/commands/encode.js';

program
	.name('fencoder')
	.description('Video encoder script utilizing FFmpeg for encoding video automatically to a subjective "best" quality standard.');

program
	.option('-a, --analyze', 'Only analyze video files, don\'t encode', false)
	.option('-r, --recursive', 'Look in subdirectories', false)
	.option('--overwrite', 'Overwrite existing analysis files', false);

program
	.argument('<files...>', 'Files to encode / directories to look through')
	.action(encode);

program.parse();
