 #ATTN:docdoom All keys i have added are verified to their proper metadatatags in ComicRack.ComicBook class
#I put them in alphabetical order (for the sake of making sure i didn't miss any)
self.allowedKeys = [
'AgeRating', #ATTN:docdoom Added String Key
'AlternateCount',
'AlternateSeries',
'AlternateNumber',
'BookNotes', #ATTN:docdoom Added String Key
'BookOwner', #ATTN:docdoom Added String Key
'BookStore', #ATTN:docdoom Added String Key
'Characters', #ATTN:docdoom Added Multi-value Key
'Colorist', #ATTN:docdoom Added Multi-value Key
'Count',
'CoverArtist', #ATTN:docdoom Added Multi-value Key
'Day', #ATTN:docdoom Added Numeric Key
'Editor', #ATTN:docdoom Added Multi-value Key
'FileDirectory',
'FileFormat', #ATTN:docdoom Added String Key (Read-Only so not valid for values)
'FileName',
'FilePath',
'Format',
'Genre',
'Imprint',
'Inker', #ATTN:docdoom Added Multi-value Key (also included in multi-value below it was the only missing one)
'ISBN', #ATTN:docdoom Added String Key
'Letterer', #ATTN:docdoom Added Multi-value Key
'Locations', #ATTN:docdoom Added Multi-value Key
'MainCharacterOrTeam',
'Month',
'Notes', #ATTN:docdoom Added String Key
'Number',
'PageCount',
'Penciller', #ATTN:docdoom Added Multi-value Key
'Publisher',
'Review', #ATTN:docdoom Added String Key
'ScanInformation', #ATTN:docdoom Added String Key
'Series',
'SeriesGroup',
'StoryArc', #ATTN:docdoom Added String Key
'Summary', #ATTN:docdoom Added String Key
'Tags',
'Teams', #ATTN:docdoom Added Multi-value Key
'Title',
'Volume',
'Web', #ATTN:docdoom Added String Key
'Writer', #ATTN:docdoom Added Multi-value Key
'Year'
]

self.numericalKeys = [
'AlternateCount',
'Count',
'Day', #ATTN:docdoom -added here and above
'Month',
'PageCount',
'Volume',
'Year',
]

self.allowedKeyModifiers = [
'Is',
'Not',
'Contains',
'Greater',
'GreaterEq',
'Less',
'LessEq',
'StartsWith',
'StartsWithAnyOf',
'ContainsAnyOf',
'NotContainsAnyOf',
'NotContains',
'ContainsAllOf']

self.allowedKeyModifiersNumeric = [
'Is',
'Range',
'Not',
'Greater',
'GreaterEq',
'Less',
'LessEq']