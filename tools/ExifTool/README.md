ExifTool by Phil Harvey (philharvey66 at gmail.com)
----------------------------------------------------------------------------

ExifTool is a customizable set of Perl modules plus a full-featured
command-line application for reading and writing meta information in a wide
variety of files, including the maker note information of many digital
cameras by various manufacturers such as Canon, Casio, DJI, FLIR, FujiFilm,
GE, HP, JVC/Victor, Kodak, Leaf, Minolta/Konica-Minolta, Nikon, Nintendo,
Olympus/Epson, Panasonic/Leica, Pentax/Asahi, Phase One, Reconyx, Ricoh,
Samsung, Sanyo, Sigma/Foveon and Sony.

Below is a list of file types and meta information formats currently
supported by ExifTool (r = read, w = write, c = create):

  File Types
  ------------+-------------+-------------+-------------+------------
  3FR   r     | DPX   r     | ISO   r     | O     r     | RAW   r/w
  3G2   r/w   | DR4   r/w/c | ITC   r     | ODP   r     | RIFF  r
  3GP   r/w   | DSS   r     | J2C   r     | ODS   r     | RSRC  r
  A     r     | DV    r     | JNG   r/w   | ODT   r     | RTF   r
  AA    r     | DVB   r/w   | JP2   r/w   | OFR   r     | RW2   r/w
  AAE   r     | DVR-MS r    | JPEG  r/w   | OGG   r     | RWL   r/w
  AAX   r/w   | DYLIB r     | JSON  r     | OGV   r     | RWZ   r
  ACR   r     | EIP   r     | K25   r     | OPUS  r     | RM    r
  AFM   r     | EPS   r/w   | KDC   r     | ORF   r/w   | SEQ   r
  AI    r/w   | EPUB  r     | KEY   r     | OTF   r     | SKETCH r
  AIFF  r     | ERF   r/w   | LA    r     | PAC   r     | SO    r
  APE   r     | EXE   r     | LFP   r     | PAGES r     | SR2   r/w
  ARQ   r/w   | EXIF  r/w/c | LNK   r     | PBM   r/w   | SRF   r
  ARW   r/w   | EXR   r     | LRV   r/w   | PCD   r     | SRW   r/w
  ASF   r     | EXV   r/w/c | M2TS  r     | PCX   r     | SVG   r
  AVI   r     | F4A/V r/w   | M4A/V r/w   | PDB   r     | SWF   r
  AVIF  r/w   | FFF   r/w   | MAX   r     | PDF   r/w   | THM   r/w
  AZW   r     | FITS  r     | MEF   r/w   | PEF   r/w   | TIFF  r/w
  BMP   r     | FLA   r     | MIE   r/w/c | PFA   r     | TORRENT r
  BPG   r     | FLAC  r     | MIFF  r     | PFB   r     | TTC   r
  BTF   r     | FLIF  r/w   | MKA   r     | PFM   r     | TTF   r
  CHM   r     | FLV   r     | MKS   r     | PGF   r     | TXT   r
  COS   r     | FPF   r     | MKV   r     | PGM   r/w   | VCF   r
  CR2   r/w   | FPX   r     | MNG   r/w   | PLIST r     | VRD   r/w/c
  CR3   r/w   | GIF   r/w   | MOBI  r     | PICT  r     | VSD   r
  CRM   r/w   | GPR   r/w   | MODD  r     | PMP   r     | WAV   r
  CRW   r/w   | GZ    r     | MOI   r     | PNG   r/w   | WDP   r/w
  CS1   r/w   | HDP   r/w   | MOS   r/w   | PPM   r/w   | WEBP  r
  CSV   r     | HDR   r     | MOV   r/w   | PPT   r     | WEBM  r
  CZI   r     | HEIC  r/w   | MP3   r     | PPTX  r     | WMA   r
  DCM   r     | HEIF  r/w   | MP4   r/w   | PS    r/w   | WMV   r
  DCP   r/w   | HTML  r     | MPC   r     | PSB   r/w   | WTV   r
  DCR   r     | ICC   r/w/c | MPG   r     | PSD   r/w   | WV    r
  DFONT r     | ICS   r     | MPO   r/w   | PSP   r     | X3F   r/w
  DIVX  r     | IDML  r     | MQV   r/w   | QTIF  r/w   | XCF   r
  DJVU  r     | IIQ   r/w   | MRW   r/w   | R3D   r     | XLS   r
  DLL   r     | IND   r/w   | MXF   r     | RA    r     | XLSX  r
  DNG   r/w   | INSP  r/w   | NEF   r/w   | RAF   r/w   | XMP   r/w/c
  DOC   r     | INSV  r     | NRW   r/w   | RAM   r     | ZIP   r
  DOCX  r     | INX   r     | NUMBERS r   | RAR   r     |

  Meta Information
  ----------------------+----------------------+---------------------
  EXIF           r/w/c  |  CIFF           r/w  |  Ricoh RMETA    r
  GPS            r/w/c  |  AFCP           r/w  |  Picture Info   r
  IPTC           r/w/c  |  Kodak Meta     r/w  |  Adobe APP14    r
  XMP            r/w/c  |  FotoStation    r/w  |  MPF            r
  MakerNotes     r/w/c  |  PhotoMechanic  r/w  |  Stim           r
  Photoshop IRB  r/w/c  |  JPEG 2000      r    |  DPX            r
  ICC Profile    r/w/c  |  DICOM          r    |  APE            r
  MIE            r/w/c  |  Flash          r    |  Vorbis         r
  JFIF           r/w/c  |  FlashPix       r    |  SPIFF          r
  Ducky APP12    r/w/c  |  QuickTime      r    |  DjVu           r
  PDF            r/w/c  |  Matroska       r    |  M2TS           r
  PNG            r/w/c  |  MXF            r    |  PE/COFF        r
  Canon VRD      r/w/c  |  PrintIM        r    |  AVCHD          r
  Nikon Capture  r/w/c  |  FLAC           r    |  ZIP            r
  GeoTIFF        r/w/c  |  ID3            r    |  (and more)

See html/index.html for more details about ExifTool features.

ExifTool can be downloaded from

  https://exiftool.org/

RUNNING

The exiftool script can be run right away without the need to install
Image::ExifTool.  For example, from within the exiftool directory you can
extract the information from one of the included test files by typing:

  ./exiftool t/images/ExifTool.jpg

If you move the exiftool script to a different directory, you must also
either move the contents of the lib directory or install the Image::ExifTool
package so the script can find the necessary libraries.

Note:  If you are using the Windows cmd shell, you may need to rename
'exiftool' to 'exiftool.pl' to run it directly from the command line.
Alternatively, you can run exiftool with the command 'perl exiftool'.

IF YOU ARE STILL CONFUSED

The exiftool script is a command line application.  You run it by typing
commands in a terminal window.  The first step is to determine the name of
the directory where you downloaded the ExifTool distribution package.
Assuming, for example, you downloaded it to a folder called "Desktop" in
your home directory, then you would type the following commands in a
terminal window to extract and run ExifTool:

  cd ~/Desktop
  gzip -dc Image-ExifTool-12.05.tar.gz | tar -xf -
  cd Image-ExifTool-12.05
  ./exiftool t/images/ExifTool.jpg

Note:  These commands extract meta information from one of the test images. 
To use one of your images instead, enter the full path name of your file in
place of "t/images/ExifTool.jpg".

INSTALLATION

You can install the Image::ExifTool package to make it available for use by
other Perl scripts by typing the following:

  perl Makefile.PL
  make
  make test
  make install

Notes:
  i) You need root access for the last step above.

  ii) Some Perl installations (like the standard OSX installation) may not
  contain the necessary files to complete the first step above.  But no
  worries:  You can install ExifTool manually by moving 'exiftool' and the
  'lib' directory to any directory in your current PATH (ie. /usr/bin).

  iii) In Windows, "dmake" or "nmake" may be used if "make" is not
  available.

(Also see html/install.html for more help with installation.)

DEPENDENCIES

Requires Perl version 5.004 or later.  No other special libraries are
required, however the following modules are recommended for decoding
compressed and/or encrypted information from the indicated file types, and
for calculating digest values and providing other features listed below:

  Archive::Zip         (ZIP, DOCX, PPTX, XLSX, ODP, ODS, ODT, EIP, iWork)
  Compress::Zlib       (DNG, PNG, PDF, DCM, MIE and SWF files)
  Digest::MD5          (PDF files, IPTC information, and JPG Extended XMP)
  Digest::SHA          (PDF with AES-256 encryption)
  IO::Compress::Bzip2  (RWZ files)
  Time::HiRes          (for generating ProcessingTime tag)
  POSIX::strptime      (for inverse date/time conversion)
  Time::Piece          (alternative to POSIX::strptime)
  Unicode::LineBreak   (for column alignment of alternate-language output)
  Win32::API           (for proper handling of Windows file times)
  Win32::FindFile      (for Windows Unicode directory support, app only)
  Win32API::File       (for Windows Unicode file names and file times)
  IO::Compress::RawDeflate   (for writing FLIF images)
  IO::Uncompress::RawInflate (for reading FLIF images)

COPYRIGHT AND LICENSE

Copyright 2003-2020, Phil Harvey

This is free software; you can redistribute it and/or modify it under the
same terms as Perl itself.

DISTRIBUTION FILES

Below is a list of the files/directories included in the full ExifTool
distribution package:

  Changes                   - Revision history
  MANIFEST                  - Full list of distribution files
  META.json                 - Standard CPAN dependency file (JSON format)
  META.yml                  - Standard CPAN dependency file (YAML format)
  Makefile.PL               - Makefile for installation
  README                    - This file
  arg_files/                - Argument files to convert metadata formats:
    exif2iptc.args            - Arguments for converting EXIF to IPTC
    exif2xmp.args             - Arguments for converting EXIF to XMP
    gps2xmp.args              - Arguments for converting GPS to XMP
    iptc2exif.args            - Arguments for converting IPTC to EXIF
    iptc2xmp.args             - Arguments for converting IPTC to XMP
    iptcCore.args             - Complete list of IPTC Core XMP tags
    pdf2xmp.args              - Arguments for converting PDF to XMP
    xmp2exif.args             - Arguments for converting XMP to EXIF
    xmp2gps.args              - Arguments for converting XMP to GPS
    xmp2iptc.args             - Arguments for converting XMP to IPTC
    xmp2pdf.args              - Arguments for converting XMP to PDF
  config_files/             - Sample ExifTool configuration files:
    acdsee.config             - Definitions for writing ACDSee XMP regions
    age.config                - Calculate Age of person in photo
    bibble.config             - Definitions for writing Bibble XMP tags
    convert_regions.config    - Convert between MWG, MP and IPTC regions
    depthmap.config           - Extract Google DepthMap images
    example.config            - General example showing config features
    fotoware.config           - Definitions for writing Fotoware XMP tags
    gps2utm.config            - Generate UTM coordinate tags from GPS info
    gpsdatetime.config        - Make GPSDateTime from CreateDate+SampleTime
    nksc.config               - Decode tags in Nikon ViewNX NKSC files
    photoshop_paths.config    - For extracting or copying Photoshop paths
    picasa_faces.config       - Convert from Picasa to MWG/MP face regions
    rotate_regions.config     - Rotate MWG and MP region tags
    tiff_version.config       - Determine the version of a TIFF file
    time_zone.config          - Calculate time zone from EXIF tags
  exiftool                  - The exiftool application (Perl script)
  fmt_files/                - Output formatting example files:
    gpx.fmt                   - Format file for creating GPX track
    gpx_wpt.fmt               - Format file for creating GPX waypoints
    kml.fmt                   - Format file for creating KML placemarks
    kml_track.fmt             - Format file for creating KML track
  html/                     - HTML documentation
  html/TagNames/            - HTML tag name documentation
  lib/                      - ExifTool Perl library modules
  perl-Image-ExifTool.spec  - Red Hat Packaging Manager specification file
  t/                        - Verification test code
  t/images/                 - Verification test images

ADDITIONAL INFORMATION

Read the following files included in the full distribution for more
information:

  html/index.html           - Main ExifTool documentation
  html/install.html         - Installation instructions
  html/history.html         - Revision history
  html/ExifTool.html        - API documentation
  html/TagNames/index.html  - Tag name documentation
  html/geotag.html          - Geotag feature
  html/faq.html             - Frequently asked questions
  html/filename.html        - Renaming/moving files
  html/metafiles.html       - Working with metadata sidecar files
  html/struct.html          - Working with structured XMP information
  lib/Image/ExifTool/README - ExifTool library modules documentation

and if you have installed Image::ExifTool, you can also consult perldoc or
the man pages:

  perldoc exiftool
  perldoc Image::ExifTool
  perldoc Image::ExifTool::TagNames

  man exiftool
  man Image::ExifTool
  man Image::ExifTool::TagNames

Note: If the man pages don't work, it is probably because your man path is
not set to include the installed documentation.  See "man man" for
information about how to set the man path.

----------------------------------------------------------------------------
