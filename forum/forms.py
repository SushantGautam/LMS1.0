# -*- coding: utf-8 -*-
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.conf import settings

from django.forms import ModelForm
from django import forms
from django.utils.translation import ugettext as _
from .models import Thread, Appendix, ForumAvatar, Post, Topic


if 'pagedown' in settings.INSTALLED_APPS:
    use_pagedown = True
    from django import forms
    from pagedown.widgets import PagedownWidget
else:
    use_pagedown = False


class ThreadForm(ModelForm):
    if use_pagedown:
        content_raw = forms.CharField(
            label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ThreadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Thread
        fields = ['topic', 'title', 'content_raw']
        labels = {
            'content_raw': _('Content'),
            'topic': _('Topic'),
            'title': _('Title'),
        }

    def save(self, commit=True):
        inst = super(ThreadForm, self).save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class ThreadEditForm(ModelForm):
    if use_pagedown:
        content_raw = forms.CharField(
            label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        super(ThreadEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Thread
        fields = ('title', 'content_raw',)
        labels = {
            'content_raw': ('Content'),
        }


class TopicForm(ModelForm):
    if use_pagedown:
        content_raw = forms.CharField(
            label=_('Content'), widget=PagedownWidget())
    TOPIC_CHOICES = [
        ("address-book", "&#xf039; &nbsp; address-book"),
        ("address-book-o", " &#xf2ba address-book-o"),
        ("address-card", " &#xf2bb address-card"),
        ("address-card-o", " &#xf2bc address-card-o"),
        ("adjust", " &#xf042 adjust"),
        ("adn", " &#xf170 adn"),
        ("align-center", " &#xf037 align-center"),
        ("align-justify", " &#xf039 align-justify"),
        ("align-left", " &#xf036 align-left"),
        ("align-right", " &#xf038 align-right"),
        ("amazon", " &#xf270 amazon"),
        ("ambulance", " &#xf0f9 ambulance"),
        ("american-sign-language-interpreting", " &#xf2a3 american-sign-language-interpreting"),
        ("anchor", " &#xf13d anchor"),
        ("android", " &#xf17b android"),
        ("angellist", " &#xf209 angellist"),
        ("angle-double-down", " &#xf103 angle-double-down"),
        ("angle-double-left", " &#xf100 angle-double-left"),
        ("angle-double-right", " &#xf101 angle-double-right"),
        ("angle-double-up", " &#xf102 angle-double-up"),
        ("angle-down", " &#xf107 angle-down"),
        ("angle-left", " &#xf104 angle-left"),
        ("angle-right", " &#xf105 angle-right"),
        ("angle-up", " &#xf106 angle-up"),
        ("apple", " &#xf179 apple"),
        ("archive", " &#xf187 archive"),
        ("area-chart", " &#xf1fe area-chart"),
        ("arrow-circle-down", " &#xf0ab arrow-circle-down"),
        ("arrow-circle-left", " &#xf0a8 arrow-circle-left"),
        ("arrow-circle-o-down", " &#xf01a arrow-circle-o-down"),
        ("arrow-circle-o-left", " &#xf190 arrow-circle-o-left"),
        ("arrow-circle-o-right", " &#xf18e arrow-circle-o-right"),
        ("arrow-circle-o-up", " &#xf01b arrow-circle-o-up"),
        ("arrow-circle-right", " &#xf0a9 arrow-circle-right"),
        ("arrow-circle-up", " &#xf0aa arrow-circle-up"),
        ("arrow-down", " &#xf063 arrow-down"),
        ("arrow-left", " &#xf060 arrow-left"),
        ("arrow-right", " &#xf061 arrow-right"),
        ("arrow-up", " &#xf062 arrow-up"),
        ("arrows", " &#xf047 arrows"),
        ("arrows-alt", " &#xf0b2 arrows-alt"),
        ("arrows-h", " &#xf07e arrows-h"),
        ("arrows-v", " &#xf07d arrows-v"),
        ("asl-interpreting", " &#xf2a3 asl-interpreting"),
        ("assistive-listening-systems", " &#xf2a2 assistive-listening-systems"),
        ("asterisk", " &#xf069 asterisk"),
        ("at", " &#xf1fa at"),
        ("audio-description", " &#xf29e audio-description"),
        ("automobile", " &#xf1b9 automobile"),
        ("backward", " &#xf04a backward"),
        ("balance-scale", " &#xf24e balance-scale"),
        ("ban", " &#xf05e ban"),
        ("bandcamp", " &#xf2d5 bandcamp"),
        ("bank", " &#xf19c bank"),
        ("bar-chart", " &#xf080 bar-chart"),
        ("bar-chart-o", " &#xf080 bar-chart-o"),
        ("barcode", " &#xf02a barcode"),
        ("bars", " &#xf0c9 bars"),
        ("bath", " &#xf2cd bath"),
        ("bathtub", " &#xf2cd bathtub"),
        ("battery", " &#xf240 battery"),
        ("battery-0", " &#xf244 battery-0"),
        ("battery-1", " &#xf243 battery-1"),
        ("battery-2", " &#xf242 battery-2"),
        ("battery-3", " &#xf241 battery-3"),
        ("battery-4", " &#xf240 battery-4"),
        ("battery-empty", " &#xf244 battery-empty"),
        ("battery-full", " &#xf240 battery-full"),
        ("battery-half", " &#xf242 battery-half"),
        ("battery-quarter", " &#xf243 battery-quarter"),
        ("battery-three-quarters", " &#xf241 battery-three-quarters"),
        ("bed", " &#xf236 bed"),
        ("beer", " &#xf0fc beer"),
        ("behance", " &#xf1b4 behance"),
        ("behance-square", " &#xf1b5 behance-square"),
        ("bell", " &#xf0f3 bell"),
        ("bell-o", " &#xf0a2 bell-o"),
        ("bell-slash", " &#xf1f6 bell-slash"),
        ("bell-slash-o", " &#xf1f7 bell-slash-o"),
        ("bicycle", " &#xf206 bicycle"),
        ("binoculars", " &#xf1e5 binoculars"),
        ("birthday-cake", " &#xf1fd birthday-cake"),
        ("bitbucket", " &#xf171 bitbucket"),
        ("bitbucket-square", " &#xf172 bitbucket-square"),
        ("bitcoin", " &#xf15a bitcoin"),
        ("black-tie", " &#xf27e black-tie"),
        ("blind", " &#xf29d blind"),
        ("bluetooth", " &#xf293 bluetooth"),
        ("bluetooth-b", " &#xf294 bluetooth-b"),
        ("bold", " &#xf032 bold"),
        ("bolt", " &#xf0e7 bolt"),
        ("bomb", " &#xf1e2 bomb"),
        ("book", " &#xf02d book"),
        ("bookmark", " &#xf02e bookmark"),
        ("bookmark-o", " &#xf097 bookmark-o"),
        ("braille", " &#xf2a1 braille"),
        ("briefcase", " &#xf0b1 briefcase"),
        ("btc", " &#xf15a btc"),
        ("bug", " &#xf188 bug"),
        ("building", " &#xf1ad building"),
        ("building-o", " &#xf0f7 building-o"),
        ("bullhorn", " &#xf0a1 bullhorn"),
        ("bullseye", " &#xf140 bullseye"),
        ("bus", " &#xf207 bus"),
        ("buysellads", " &#xf20d buysellads"),
        ("cab", " &#xf1ba cab"),
        ("calculator", " &#xf1ec calculator"),
        ("calendar", " &#xf073 calendar"),
        ("calendar-check-o", " &#xf274 calendar-check-o"),
        ("calendar-minus-o", " &#xf272 calendar-minus-o"),
        ("calendar-o", " &#xf133 calendar-o"),
        ("calendar-plus-o", " &#xf271 calendar-plus-o"),
        ("calendar-times-o", " &#xf273 calendar-times-o"),
        ("camera", " &#xf030 camera"),
        ("camera-retro", " &#xf083 camera-retro"),
        ("car", " &#xf1b9 car"),
        ("caret-down", " &#xf0d7 caret-down"),
        ("caret-left", " &#xf0d9 caret-left"),
        ("caret-right", " &#xf0da caret-right"),
        ("caret-square-o-down", " &#xf150 caret-square-o-down"),
        ("caret-square-o-left", " &#xf191 caret-square-o-left"),
        ("caret-square-o-right", " &#xf152 caret-square-o-right"),
        ("caret-square-o-up", " &#xf151 caret-square-o-up"),
        ("caret-up", " &#xf0d8 caret-up"),
        ("cart-arrow-down", " &#xf218 cart-arrow-down"),
        ("cart-plus", " &#xf217 cart-plus"),
        ("cc", " &#xf20a cc"),
        ("cc-amex", " &#xf1f3 cc-amex"),
        ("cc-diners-club", " &#xf24c cc-diners-club"),
        ("cc-discover", " &#xf1f2 cc-discover"),
        ("cc-jcb", " &#xf24b cc-jcb"),
        ("cc-mastercard", " &#xf1f1 cc-mastercard"),
        ("cc-paypal", " &#xf1f4 cc-paypal"),
        ("cc-stripe", " &#xf1f5 cc-stripe"),
        ("cc-visa", " &#xf1f0 cc-visa"),
        ("certificate", " &#xf0a3 certificate"),
        ("chain", " &#xf0c1 chain"),
        ("chain-broken", " &#xf127 chain-broken"),
        ("check", " &#xf00c check"),
        ("check-circle", " &#xf058 check-circle"),
        ("check-circle-o", " &#xf05d check-circle-o"),
        ("check-square", " &#xf14a check-square"),
        ("check-square-o", " &#xf046 check-square-o"),
        ("chevron-circle-down", " &#xf13a chevron-circle-down"),
        ("chevron-circle-left", " &#xf137 chevron-circle-left"),
        ("chevron-circle-right", " &#xf138 chevron-circle-right"),
        ("chevron-circle-up", " &#xf139 chevron-circle-up"),
        ("chevron-down", " &#xf078 chevron-down"),
        ("chevron-left", " &#xf053 chevron-left"),
        ("chevron-right", " &#xf054 chevron-right"),
        ("chevron-up", " &#xf077 chevron-up"),
        ("child", " &#xf1ae child"),
        ("chrome", " &#xf268 chrome"),
        ("circle", " &#xf111 circle"),
        ("circle-o", " &#xf10c circle-o"),
        ("circle-o-notch", " &#xf1ce circle-o-notch"),
        ("circle-thin", " &#xf1db circle-thin"),
        ("clipboard", " &#xf0ea clipboard"),
        ("clock-o", " &#xf017 clock-o"),
        ("clone", " &#xf24d clone"),
        ("close", " &#xf00d close"),
        ("cloud", " &#xf0c2 cloud"),
        ("cloud-download", " &#xf0ed cloud-download"),
        ("cloud-upload", " &#xf0ee cloud-upload"),
        ("cny", " &#xf157 cny"),
        ("code", " &#xf121 code"),
        ("code-fork", " &#xf126 code-fork"),
        ("codepen", " &#xf1cb codepen"),
        ("codiepie", " &#xf284 codiepie"),
        ("coffee", " &#xf0f4 coffee"),
        ("cog", " &#xf013 cog"),
        ("cogs", " &#xf085 cogs"),
        ("columns", " &#xf0db columns"),
        ("comment", " &#xf075 comment"),
        ("comment-o", " &#xf0e5 comment-o"),
        ("commenting", " &#xf27a commenting"),
        ("commenting-o", " &#xf27b commenting-o"),
        ("comments", " &#xf086 comments"),
        ("comments-o", " &#xf0e6 comments-o"),
        ("compass", " &#xf14e compass"),
        ("compress", " &#xf066 compress"),
        ("connectdevelop", " &#xf20e connectdevelop"),
        ("contao", " &#xf26d contao"),
        ("copy", " &#xf0c5 copy"),
        ("copyright", " &#xf1f9 copyright"),
        ("creative-commons", " &#xf25e creative-commons"),
        ("credit-card", " &#xf09d credit-card"),
        ("credit-card-alt", " &#xf283 credit-card-alt"),
        ("crop", " &#xf125 crop"),
        ("crosshairs", " &#xf05b crosshairs"),
        ("css3", " &#xf13c css3"),
        ("cube", " &#xf1b2 cube"),
        ("cubes", " &#xf1b3 cubes"),
        ("cut", " &#xf0c4 cut"),
        ("cutlery", " &#xf0f5 cutlery"),
        ("dashboard", " &#xf0e4 dashboard"),
        ("dashcube", " &#xf210 dashcube"),
        ("database", " &#xf1c0 database"),
        ("deaf", " &#xf2a4 deaf"),
        ("deafness", " &#xf2a4 deafness"),
        ("dedent", " &#xf03b dedent"),
        ("delicious", " &#xf1a5 delicious"),
        ("desktop", " &#xf108 desktop"),
        ("deviantart", " &#xf1bd deviantart"),
        ("diamond", " &#xf219 diamond"),
        ("digg", " &#xf1a6 digg"),
        ("dollar", " &#xf155 dollar"),
        ("dot-circle-o", " &#xf192 dot-circle-o"),
        ("download", " &#xf019 download"),
        ("dribbble", " &#xf17d dribbble"),
        ("drivers-license", " &#xf2c2 drivers-license"),
        ("drivers-license-o", " &#xf2c3 drivers-license-o"),
        ("dropbox", " &#xf16b dropbox"),
        ("drupal", " &#xf1a9 drupal"),
        ("edge", " &#xf282 edge"),
        ("edit", " &#xf044 edit"),
        ("eercast", " &#xf2da eercast"),
        ("eject", " &#xf052 eject"),
        ("ellipsis-h", " &#xf141 ellipsis-h"),
        ("ellipsis-v", " &#xf142 ellipsis-v"),
        ("empire", " &#xf1d1 empire"),
        ("envelope", " &#xf0e0 envelope"),
        ("envelope-o", " &#xf003 envelope-o"),
        ("envelope-open", " &#xf2b6 envelope-open"),
        ("envelope-open-o", " &#xf2b7 envelope-open-o"),
        ("envelope-square", " &#xf199 envelope-square"),
        ("envira", " &#xf299 envira"),
        ("eraser", " &#xf12d eraser"),
        ("etsy", " &#xf2d7 etsy"),
        ("eur", " &#xf153 eur"),
        ("euro", " &#xf153 euro"),
        ("exchange", " &#xf0ec exchange"),
        ("exclamation", " &#xf12a exclamation"),
        ("exclamation-circle", " &#xf06a exclamation-circle"),
        ("exclamation-triangle", " &#xf071 exclamation-triangle"),
        ("expand", " &#xf065 expand"),
        ("expeditedssl", " &#xf23e expeditedssl"),
        ("external-link", " &#xf08e external-link"),
        ("external-link-square", " &#xf14c external-link-square"),
        ("eye", " &#xf06e eye"),
        ("eye-slash", " &#xf070 eye-slash"),
        ("eyedropper", " &#xf1fb eyedropper"),
        ("fa", " &#xf2b4 fa"),
        ("facebook", " &#xf09a facebook"),
        ("facebook-f", " &#xf09a facebook-f"),
        ("facebook-official", " &#xf230 facebook-official"),
        ("facebook-square", " &#xf082 facebook-square"),
        ("fast-backward", " &#xf049 fast-backward"),
        ("fast-forward", " &#xf050 fast-forward"),
        ("fax", " &#xf1ac fax"),
        ("feed", " &#xf09e feed"),
        ("female", " &#xf182 female"),
        ("fighter-jet", " &#xf0fb fighter-jet"),
        ("file", " &#xf15b file"),
        ("file-archive-o", " &#xf1c6 file-archive-o"),
        ("file-audio-o", " &#xf1c7 file-audio-o"),
        ("file-code-o", " &#xf1c9 file-code-o"),
        ("file-excel-o", " &#xf1c3 file-excel-o"),
        ("file-image-o", " &#xf1c5 file-image-o"),
        ("file-movie-o", " &#xf1c8 file-movie-o"),
        ("file-o", " &#xf016 file-o"),
        ("file-pdf-o", " &#xf1c1 file-pdf-o"),
        ("file-photo-o", " &#xf1c5 file-photo-o"),
        ("file-picture-o", " &#xf1c5 file-picture-o"),
        ("file-powerpoint-o", " &#xf1c4 file-powerpoint-o"),
        ("file-sound-o", " &#xf1c7 file-sound-o"),
        ("file-text", " &#xf15c file-text"),
        ("file-text-o", " &#xf0f6 file-text-o"),
        ("file-video-o", " &#xf1c8 file-video-o"),
        ("file-word-o", " &#xf1c2 file-word-o"),
        ("file-zip-o", " &#xf1c6 file-zip-o"),
        ("files-o", " &#xf0c5 files-o"),
        ("film", " &#xf008 film"),
        ("filter", " &#xf0b0 filter"),
        ("fire", " &#xf06d fire"),
        ("fire-extinguisher", " &#xf134 fire-extinguisher"),
        ("firefox", " &#xf269 firefox"),
        ("first-order", " &#xf2b0 first-order"),
        ("flag", " &#xf024 flag"),
        ("flag-checkered", " &#xf11e flag-checkered"),
        ("flag-o", " &#xf11d flag-o"),
        ("flash", " &#xf0e7 flash"),
        ("flask", " &#xf0c3 flask"),
        ("flickr", " &#xf16e flickr"),
        ("floppy-o", " &#xf0c7 floppy-o"),
        ("folder", " &#xf07b folder"),
        ("folder-o", " &#xf114 folder-o"),
        ("folder-open", " &#xf07c folder-open"),
        ("folder-open-o", " &#xf115 folder-open-o"),
        ("font", " &#xf031 font"),
        ("font-awesome", " &#xf2b4 font-awesome"),
        ("fonticons", " &#xf280 fonticons"),
        ("fort-awesome", " &#xf286 fort-awesome"),
        ("forumbee", " &#xf211 forumbee"),
        ("forward", " &#xf04e forward"),
        ("foursquare", " &#xf180 foursquare"),
        ("free-code-camp", " &#xf2c5 free-code-camp"),
        ("frown-o", " &#xf119 frown-o"),
        ("futbol-o", " &#xf1e3 futbol-o"),
        ("gamepad", " &#xf11b gamepad"),
        ("gavel", " &#xf0e3 gavel"),
        ("gbp", " &#xf154 gbp"),
        ("ge", " &#xf1d1 ge"),
        ("gear", " &#xf013 gear"),
        ("gears", " &#xf085 gears"),
        ("genderless", " &#xf22d genderless"),
        ("get-pocket", " &#xf265 get-pocket"),
        ("gg", " &#xf260 gg"),
        ("gg-circle", " &#xf261 gg-circle"),
        ("gift", " &#xf06b gift"),
        ("git", " &#xf1d3 git"),
        ("git-square", " &#xf1d2 git-square"),
        ("github", " &#xf09b github"),
        ("github-alt", " &#xf113 github-alt"),
        ("github-square", " &#xf092 github-square"),
        ("gitlab", " &#xf296 gitlab"),
        ("gittip", " &#xf184 gittip"),
        ("glass", " &#xf000 glass"),
        ("glide", " &#xf2a5 glide"),
        ("glide-g", " &#xf2a6 glide-g"),
        ("globe", " &#xf0ac globe"),
        ("google", " &#xf1a0 google"),
        ("google-plus", " &#xf0d5 google-plus"),
        ("google-plus-circle", " &#xf2b3 google-plus-circle"),
        ("google-plus-official", " &#xf2b3 google-plus-official"),
        ("google-plus-square", " &#xf0d4 google-plus-square"),
        ("google-wallet", " &#xf1ee google-wallet"),
        ("graduation-cap", " &#xf19d graduation-cap"),
        ("gratipay", " &#xf184 gratipay"),
        ("grav", " &#xf2d6 grav"),
        ("group", " &#xf0c0 group"),
        ("h-square", " &#xf0fd h-square"),
        ("hacker-news", " &#xf1d4 hacker-news"),
        ("hand-grab-o", " &#xf255 hand-grab-o"),
        ("hand-lizard-o", " &#xf258 hand-lizard-o"),
        ("hand-o-down", " &#xf0a7 hand-o-down"),
        ("hand-o-left", " &#xf0a5 hand-o-left"),
        ("hand-o-right", " &#xf0a4 hand-o-right"),
        ("hand-o-up", " &#xf0a6 hand-o-up"),
        ("hand-paper-o", " &#xf256 hand-paper-o"),
        ("hand-peace-o", " &#xf25b hand-peace-o"),
        ("hand-pointer-o", " &#xf25a hand-pointer-o"),
        ("hand-rock-o", " &#xf255 hand-rock-o"),
        ("hand-scissors-o", " &#xf257 hand-scissors-o"),
        ("hand-spock-o", " &#xf259 hand-spock-o"),
        ("hand-stop-o", " &#xf256 hand-stop-o"),
        ("handshake-o", " &#xf2b5 handshake-o"),
        ("hard-of-hearing", " &#xf2a4 hard-of-hearing"),
        ("hashtag", " &#xf292 hashtag"),
        ("hdd-o", " &#xf0a0 hdd-o"),
        ("header", " &#xf1dc header"),
        ("headphones", " &#xf025 headphones"),
        ("heart", " &#xf004 heart"),
        ("heart-o", " &#xf08a heart-o"),
        ("heartbeat", " &#xf21e heartbeat"),
        ("history", " &#xf1da history"),
        ("home", " &#xf015 home"),
        ("hospital-o", " &#xf0f8 hospital-o"),
        ("hotel", " &#xf236 hotel"),
        ("hourglass", " &#xf254 hourglass"),
        ("hourglass-1", " &#xf251 hourglass-1"),
        ("hourglass-2", " &#xf252 hourglass-2"),
        ("hourglass-3", " &#xf253 hourglass-3"),
        ("hourglass-end", " &#xf253 hourglass-end"),
        ("hourglass-half", " &#xf252 hourglass-half"),
        ("hourglass-o", " &#xf250 hourglass-o"),
        ("hourglass-start", " &#xf251 hourglass-start"),
        ("houzz", " &#xf27c houzz"),
        ("html5", " &#xf13b html5"),
        ("i-cursor", " &#xf246 i-cursor"),
        ("id-badge", " &#xf2c1 id-badge"),
        ("id-card", " &#xf2c2 id-card"),
        ("id-card-o", " &#xf2c3 id-card-o"),
        ("ils", " &#xf20b ils"),
        ("image", " &#xf03e image"),
        ("imdb", " &#xf2d8 imdb"),
        ("inbox", " &#xf01c inbox"),
        ("indent", " &#xf03c indent"),
        ("industry", " &#xf275 industry"),
        ("info", " &#xf129 info"),
        ("info-circle", " &#xf05a info-circle"),
        ("inr", " &#xf156 inr"),
        ("instagram", " &#xf16d instagram"),
        ("institution", " &#xf19c institution"),
        ("internet-explorer", " &#xf26b internet-explorer"),
        ("intersex", " &#xf224 intersex"),
        ("ioxhost", " &#xf208 ioxhost"),
        ("italic", " &#xf033 italic"),
        ("joomla", " &#xf1aa joomla"),
        ("jpy", " &#xf157 jpy"),
        ("jsfiddle", " &#xf1cc jsfiddle"),
        ("key", " &#xf084 key"),
        ("keyboard-o", " &#xf11c keyboard-o"),
        ("krw", " &#xf159 krw"),
        ("language", " &#xf1ab language"),
        ("laptop", " &#xf109 laptop"),
        ("lastfm", " &#xf202 lastfm"),
        ("lastfm-square", " &#xf203 lastfm-square"),
        ("leaf", " &#xf06c leaf"),
        ("leanpub", " &#xf212 leanpub"),
        ("legal", " &#xf0e3 legal"),
        ("lemon-o", " &#xf094 lemon-o"),
        ("level-down", " &#xf149 level-down"),
        ("level-up", " &#xf148 level-up"),
        ("life-bouy", " &#xf1cd life-bouy"),
        ("life-buoy", " &#xf1cd life-buoy"),
        ("life-ring", " &#xf1cd life-ring"),
        ("life-saver", " &#xf1cd life-saver"),
        ("lightbulb-o", " &#xf0eb lightbulb-o"),
        ("line-chart", " &#xf201 line-chart"),
        ("link", " &#xf0c1 link"),
        ("linkedin", " &#xf0e1 linkedin"),
        ("linkedin-square", " &#xf08c linkedin-square"),
        ("linode", " &#xf2b8 linode"),
        ("linux", " &#xf17c linux"),
        ("list", " &#xf03a list"),
        ("list-alt", " &#xf022 list-alt"),
        ("list-ol", " &#xf0cb list-ol"),
        ("list-ul", " &#xf0ca list-ul"),
        ("location-arrow", " &#xf124 location-arrow"),
        ("lock", " &#xf023 lock"),
        ("long-arrow-down", " &#xf175 long-arrow-down"),
        ("long-arrow-left", " &#xf177 long-arrow-left"),
        ("long-arrow-right", " &#xf178 long-arrow-right"),
        ("long-arrow-up", " &#xf176 long-arrow-up"),
        ("low-vision", " &#xf2a8 low-vision"),
        ("magic", " &#xf0d0 magic"),
        ("magnet", " &#xf076 magnet"),
        ("mail-forward", " &#xf064 mail-forward"),
        ("mail-reply", " &#xf112 mail-reply"),
        ("mail-reply-all", " &#xf122 mail-reply-all"),
        ("male", " &#xf183 male"),
        ("map", " &#xf279 map"),
        ("map-marker", " &#xf041 map-marker"),
        ("map-o", " &#xf278 map-o"),
        ("map-pin", " &#xf276 map-pin"),
        ("map-signs", " &#xf277 map-signs"),
        ("mars", " &#xf222 mars"),
        ("mars-double", " &#xf227 mars-double"),
        ("mars-stroke", " &#xf229 mars-stroke"),
        ("mars-stroke-h", " &#xf22b mars-stroke-h"),
        ("mars-stroke-v", " &#xf22a mars-stroke-v"),
        ("maxcdn", " &#xf136 maxcdn"),
        ("meanpath", " &#xf20c meanpath"),
        ("medium", " &#xf23a medium"),
        ("medkit", " &#xf0fa medkit"),
        ("meetup", " &#xf2e0 meetup"),
        ("meh-o", " &#xf11a meh-o"),
        ("mercury", " &#xf223 mercury"),
        ("microchip", " &#xf2db microchip"),
        ("microphone", " &#xf130 microphone"),
        ("microphone-slash", " &#xf131 microphone-slash"),
        ("minus", " &#xf068 minus"),
        ("minus-circle", " &#xf056 minus-circle"),
        ("minus-square", " &#xf146 minus-square"),
        ("minus-square-o", " &#xf147 minus-square-o"),
        ("mixcloud", " &#xf289 mixcloud"),
        ("mobile", " &#xf10b mobile"),
        ("mobile-phone", " &#xf10b mobile-phone"),
        ("modx", " &#xf285 modx"),
        ("money", " &#xf0d6 money"),
        ("moon-o", " &#xf186 moon-o"),
        ("mortar-board", " &#xf19d mortar-board"),
        ("motorcycle", " &#xf21c motorcycle"),
        ("mouse-pointer", " &#xf245 mouse-pointer"),
        ("music", " &#xf001 music"),
        ("navicon", " &#xf0c9 navicon"),
        ("neuter", " &#xf22c neuter"),
        ("newspaper-o", " &#xf1ea newspaper-o"),
        ("object-group", " &#xf247 object-group"),
        ("object-ungroup", " &#xf248 object-ungroup"),
        ("odnoklassniki", " &#xf263 odnoklassniki"),
        ("odnoklassniki-square", " &#xf264 odnoklassniki-square"),
        ("opencart", " &#xf23d opencart"),
        ("openid", " &#xf19b openid"),
        ("opera", " &#xf26a opera"),
        ("optin-monster", " &#xf23c optin-monster"),
        ("outdent", " &#xf03b outdent"),
        ("pagelines", " &#xf18c pagelines"),
        ("paint-brush", " &#xf1fc paint-brush"),
        ("paper-plane", " &#xf1d8 paper-plane"),
        ("paper-plane-o", " &#xf1d9 paper-plane-o"),
        ("paperclip", " &#xf0c6 paperclip"),
        ("paragraph", " &#xf1dd paragraph"),
        ("paste", " &#xf0ea paste"),
        ("pause", " &#xf04c pause"),
        ("pause-circle", " &#xf28b pause-circle"),
        ("pause-circle-o", " &#xf28c pause-circle-o"),
        ("paw", " &#xf1b0 paw"),
        ("paypal", " &#xf1ed paypal"),
        ("pencil", " &#xf040 pencil"),
        ("pencil-square", " &#xf14b pencil-square"),
        ("pencil-square-o", " &#xf044 pencil-square-o"),
        ("percent", " &#xf295 percent"),
        ("phone", " &#xf095 phone"),
        ("phone-square", " &#xf098 phone-square"),
        ("photo", " &#xf03e photo"),
        ("picture-o", " &#xf03e picture-o"),
        ("pie-chart", " &#xf200 pie-chart"),
        ("pied-piper", " &#xf2ae pied-piper"),
        ("pied-piper-alt", " &#xf1a8 pied-piper-alt"),
        ("pied-piper-pp", " &#xf1a7 pied-piper-pp"),
        ("pinterest", " &#xf0d2 pinterest"),
        ("pinterest-p", " &#xf231 pinterest-p"),
        ("pinterest-square", " &#xf0d3 pinterest-square"),
        ("plane", " &#xf072 plane"),
        ("play", " &#xf04b play"),
        ("play-circle", " &#xf144 play-circle"),
        ("play-circle-o", " &#xf01d play-circle-o"),
        ("plug", " &#xf1e6 plug"),
        ("plus", " &#xf067 plus"),
        ("plus-circle", " &#xf055 plus-circle"),
        ("plus-square", " &#xf0fe plus-square"),
        ("plus-square-o", " &#xf196 plus-square-o"),
        ("podcast", " &#xf2ce podcast"),
        ("power-off", " &#xf011 power-off"),
        ("print", " &#xf02f print"),
        ("product-hunt", " &#xf288 product-hunt"),
        ("puzzle-piece", " &#xf12e puzzle-piece"),
        ("qq", " &#xf1d6 qq"),
        ("qrcode", " &#xf029 qrcode"),
        ("question", " &#xf128 question"),
        ("question-circle", " &#xf059 question-circle"),
        ("question-circle-o", " &#xf29c question-circle-o"),
        ("quora", " &#xf2c4 quora"),
        ("quote-left", " &#xf10d quote-left"),
        ("quote-right", " &#xf10e quote-right"),
        ("ra", " &#xf1d0 ra"),
        ("random", " &#xf074 random"),
        ("ravelry", " &#xf2d9 ravelry"),
        ("rebel", " &#xf1d0 rebel"),
        ("recycle", " &#xf1b8 recycle"),
        ("reddit", " &#xf1a1 reddit"),
        ("reddit-alien", " &#xf281 reddit-alien"),
        ("reddit-square", " &#xf1a2 reddit-square"),
        ("refresh", " &#xf021 refresh"),
        ("registered", " &#xf25d registered"),
        ("remove", " &#xf00d remove"),
        ("renren", " &#xf18b renren"),
        ("reorder", " &#xf0c9 reorder"),
        ("repeat", " &#xf01e repeat"),
        ("reply", " &#xf112 reply"),
        ("reply-all", " &#xf122 reply-all"),
        ("resistance", " &#xf1d0 resistance"),
        ("retweet", " &#xf079 retweet"),
        ("rmb", " &#xf157 rmb"),
        ("road", " &#xf018 road"),
        ("rocket", " &#xf135 rocket"),
        ("rotate-left", " &#xf0e2 rotate-left"),
        ("rotate-right", " &#xf01e rotate-right"),
        ("rouble", " &#xf158 rouble"),
        ("rss", " &#xf09e rss"),
        ("rss-square", " &#xf143 rss-square"),
        ("rub", " &#xf158 rub"),
        ("ruble", " &#xf158 ruble"),
        ("rupee", " &#xf156 rupee"),
        ("s15", " &#xf2cd s15"),
        ("safari", " &#xf267 safari"),
        ("save", " &#xf0c7 save"),
        ("scissors", " &#xf0c4 scissors"),
        ("scribd", " &#xf28a scribd"),
        ("search", " &#xf002 search"),
        ("search-minus", " &#xf010 search-minus"),
        ("search-plus", " &#xf00e search-plus"),
        ("sellsy", " &#xf213 sellsy"),
        ("send", " &#xf1d8 send"),
        ("send-o", " &#xf1d9 send-o"),
        ("server", " &#xf233 server"),
        ("share", " &#xf064 share"),
        ("share-alt", " &#xf1e0 share-alt"),
        ("share-alt-square", " &#xf1e1 share-alt-square"),
        ("share-square", " &#xf14d share-square"),
        ("share-square-o", " &#xf045 share-square-o"),
        ("shekel", " &#xf20b shekel"),
        ("sheqel", " &#xf20b sheqel"),
        ("shield", " &#xf132 shield"),
        ("ship", " &#xf21a ship"),
        ("shirtsinbulk", " &#xf214 shirtsinbulk"),
        ("shopping-bag", " &#xf290 shopping-bag"),
        ("shopping-basket", " &#xf291 shopping-basket"),
        ("shopping-cart", " &#xf07a shopping-cart"),
        ("shower", " &#xf2cc shower"),
        ("sign-in", " &#xf090 sign-in"),
        ("sign-language", " &#xf2a7 sign-language"),
        ("sign-out", " &#xf08b sign-out"),
        ("signal", " &#xf012 signal"),
        ("signing", " &#xf2a7 signing"),
        ("simplybuilt", " &#xf215 simplybuilt"),
        ("sitemap", " &#xf0e8 sitemap"),
        ("skyatlas", " &#xf216 skyatlas"),
        ("skype", " &#xf17e skype"),
        ("slack", " &#xf198 slack"),
        ("sliders", " &#xf1de sliders"),
        ("slideshare", " &#xf1e7 slideshare"),
        ("smile-o", " &#xf118 smile-o"),
        ("snapchat", " &#xf2ab snapchat"),
        ("snapchat-ghost", " &#xf2ac snapchat-ghost"),
        ("snapchat-square", " &#xf2ad snapchat-square"),
        ("snowflake-o", " &#xf2dc snowflake-o"),
        ("soccer-ball-o", " &#xf1e3 soccer-ball-o"),
        ("sort", " &#xf0dc sort"),
        ("sort-alpha-asc", " &#xf15d sort-alpha-asc"),
        ("sort-alpha-desc", " &#xf15e sort-alpha-desc"),
        ("sort-amount-asc", " &#xf160 sort-amount-asc"),
        ("sort-amount-desc", " &#xf161 sort-amount-desc"),
        ("sort-asc", " &#xf0de sort-asc"),
        ("sort-desc", " &#xf0dd sort-desc"),
        ("sort-down", " &#xf0dd sort-down"),
        ("sort-numeric-asc", " &#xf162 sort-numeric-asc"),
        ("sort-numeric-desc", " &#xf163 sort-numeric-desc"),
        ("sort-up", " &#xf0de sort-up"),
        ("soundcloud", " &#xf1be soundcloud"),
        ("space-shuttle", " &#xf197 space-shuttle"),
        ("spinner", " &#xf110 spinner"),
        ("spoon", " &#xf1b1 spoon"),
        ("spotify", " &#xf1bc spotify"),
        ("square", " &#xf0c8 square"),
        ("square-o", " &#xf096 square-o"),
        ("stack-exchange", " &#xf18d stack-exchange"),
        ("stack-overflow", " &#xf16c stack-overflow"),
        ("star", " &#xf005 star"),
        ("star-half", " &#xf089 star-half"),
        ("star-half-empty", " &#xf123 star-half-empty"),
        ("star-half-full", " &#xf123 star-half-full"),
        ("star-half-o", " &#xf123 star-half-o"),
        ("star-o", " &#xf006 star-o"),
        ("steam", " &#xf1b6 steam"),
        ("steam-square", " &#xf1b7 steam-square"),
        ("step-backward", " &#xf048 step-backward"),
        ("step-forward", " &#xf051 step-forward"),
        ("stethoscope", " &#xf0f1 stethoscope"),
        ("sticky-note", " &#xf249 sticky-note"),
        ("sticky-note-o", " &#xf24a sticky-note-o"),
        ("stop", " &#xf04d stop"),
        ("stop-circle", " &#xf28d stop-circle"),
        ("stop-circle-o", " &#xf28e stop-circle-o"),
        ("street-view", " &#xf21d street-view"),
        ("strikethrough", " &#xf0cc strikethrough"),
        ("stumbleupon", " &#xf1a4 stumbleupon"),
        ("stumbleupon-circle", " &#xf1a3 stumbleupon-circle"),
        ("subscript", " &#xf12c subscript"),
        ("subway", " &#xf239 subway"),
        ("suitcase", " &#xf0f2 suitcase"),
        ("sun-o", " &#xf185 sun-o"),
        ("superpowers", " &#xf2dd superpowers"),
        ("superscript", " &#xf12b superscript"),
        ("support", " &#xf1cd support"),
        ("table", " &#xf0ce table"),
        ("tablet", " &#xf10a tablet"),
        ("tachometer", " &#xf0e4 tachometer"),
        ("tag", " &#xf02b tag"),
        ("tags", " &#xf02c tags"),
        ("tasks", " &#xf0ae tasks"),
        ("taxi", " &#xf1ba taxi"),
        ("telegram", " &#xf2c6 telegram"),
        ("television", " &#xf26c television"),
        ("tencent-weibo", " &#xf1d5 tencent-weibo"),
        ("terminal", " &#xf120 terminal"),
        ("text-height", " &#xf034 text-height"),
        ("text-width", " &#xf035 text-width"),
        ("th", " &#xf00a th"),
        ("th-large", " &#xf009 th-large"),
        ("th-list", " &#xf00b th-list"),
        ("themeisle", " &#xf2b2 themeisle"),
        ("thermometer", " &#xf2c7 thermometer"),
        ("thermometer-0", " &#xf2cb thermometer-0"),
        ("thermometer-1", " &#xf2ca thermometer-1"),
        ("thermometer-2", " &#xf2c9 thermometer-2"),
        ("thermometer-3", " &#xf2c8 thermometer-3"),
        ("thermometer-4", " &#xf2c7 thermometer-4"),
        ("thermometer-empty", " &#xf2cb thermometer-empty"),
        ("thermometer-full", " &#xf2c7 thermometer-full"),
        ("thermometer-half", " &#xf2c9 thermometer-half"),
        ("thermometer-quarter", " &#xf2ca thermometer-quarter"),
        ("thermometer-three-quarters", " &#xf2c8 thermometer-three-quarters"),
        ("thumb-tack", " &#xf08d thumb-tack"),
        ("thumbs-down", " &#xf165 thumbs-down"),
        ("thumbs-o-down", " &#xf088 thumbs-o-down"),
        ("thumbs-o-up", " &#xf087 thumbs-o-up"),
        ("thumbs-up", " &#xf164 thumbs-up"),
        ("ticket", " &#xf145 ticket"),
        ("times", " &#xf00d times"),
        ("times-circle", " &#xf057 times-circle"),
        ("times-circle-o", " &#xf05c times-circle-o"),
        ("times-rectangle", " &#xf2d3 times-rectangle"),
        ("times-rectangle-o", " &#xf2d4 times-rectangle-o"),
        ("tint", " &#xf043 tint"),
        ("toggle-down", " &#xf150 toggle-down"),
        ("toggle-left", " &#xf191 toggle-left"),
        ("toggle-off", " &#xf204 toggle-off"),
        ("toggle-on", " &#xf205 toggle-on"),
        ("toggle-right", " &#xf152 toggle-right"),
        ("toggle-up", " &#xf151 toggle-up"),
        ("trademark", " &#xf25c trademark"),
        ("train", " &#xf238 train"),
        ("transgender", " &#xf224 transgender"),
        ("transgender-alt", " &#xf225 transgender-alt"),
        ("trash", " &#xf1f8 trash"),
        ("trash-o", " &#xf014 trash-o"),
        ("tree", " &#xf1bb tree"),
        ("trello", " &#xf181 trello"),
        ("tripadvisor", " &#xf262 tripadvisor"),
        ("trophy", " &#xf091 trophy"),
        ("truck", " &#xf0d1 truck"),
        ("try", " &#xf195 try"),
        ("tty", " &#xf1e4 tty"),
        ("tumblr", " &#xf173 tumblr"),
        ("tumblr-square", " &#xf174 tumblr-square"),
        ("turkish-lira", " &#xf195 turkish-lira"),
        ("tv", " &#xf26c tv"),
        ("twitch", " &#xf1e8 twitch"),
        ("twitter", " &#xf099 twitter"),
        ("twitter-square", " &#xf081 twitter-square"),
        ("umbrella", " &#xf0e9 umbrella"),
        ("underline", " &#xf0cd underline"),
        ("undo", " &#xf0e2 undo"),
        ("universal-access", " &#xf29a universal-access"),
        ("university", " &#xf19c university"),
        ("unlink", " &#xf127 unlink"),
        ("unlock", " &#xf09c unlock"),
        ("unlock-alt", " &#xf13e unlock-alt"),
        ("unsorted", " &#xf0dc unsorted"),
        ("upload", " &#xf093 upload"),
        ("usb", " &#xf287 usb"),
        ("usd", " &#xf155 usd"),
        ("user", " &#xf007 user"),
        ("user-circle", " &#xf2bd user-circle"),
        ("user-circle-o", " &#xf2be user-circle-o"),
        ("user-md", " &#xf0f0 user-md"),
        ("user-o", " &#xf2c0 user-o"),
        ("user-plus", " &#xf234 user-plus"),
        ("user-secret", " &#xf21b user-secret"),
        ("user-times", " &#xf235 user-times"),
        ("users", " &#xf0c0 users"),
        ("vcard", " &#xf2bb vcard"),
        ("vcard-o", " &#xf2bc vcard-o"),
        ("venus", " &#xf221 venus"),
        ("venus-double", " &#xf226 venus-double"),
        ("venus-mars", " &#xf228 venus-mars"),
        ("viacoin", " &#xf237 viacoin"),
        ("viadeo", " &#xf2a9 viadeo"),
        ("viadeo-square", " &#xf2aa viadeo-square"),
        ("video-camera", " &#xf03d video-camera"),
        ("vimeo", " &#xf27d vimeo"),
        ("vimeo-square", " &#xf194 vimeo-square"),
        ("vine", " &#xf1ca vine"),
        ("vk", " &#xf189 vk"),
        ("volume-control-phone", " &#xf2a0 volume-control-phone"),
        ("volume-down", " &#xf027 volume-down"),
        ("volume-off", " &#xf026 volume-off"),
        ("volume-up", " &#xf028 volume-up"),
        ("warning", " &#xf071 warning"),
        ("wechat", " &#xf1d7 wechat"),
        ("weibo", " &#xf18a weibo"),
        ("weixin", " &#xf1d7 weixin"),
        ("whatsapp", " &#xf232 whatsapp"),
        ("wheelchair", " &#xf193 wheelchair"),
        ("wheelchair-alt", " &#xf29b wheelchair-alt"),
        ("wifi", " &#xf1eb wifi"),
        ("wikipedia-w", " &#xf266 wikipedia-w"),
        ("window-close", " &#xf2d3 window-close"),
        ("window-close-o", " &#xf2d4 window-close-o"),
        ("window-maximize", " &#xf2d0 window-maximize"),
        ("window-minimize", " &#xf2d1 window-minimize"),
        ("window-restore", " &#xf2d2 window-restore"),
        ("windows", " &#xf17a windows"),
        ("won", " &#xf159 won"),
        ("wordpress", " &#xf19a wordpress"),
        ("wpbeginner", " &#xf297 wpbeginner"),
        ("wpexplorer", " &#xf2de wpexplorer"),
        ("wpforms", " &#xf298 wpforms"),
        ("wrench", " &#xf0ad wrench"),
        ("xing", " &#xf168 xing"),
        ("xing-square", " &#xf169 xing-square"),
        ("y-combinator", " &#xf23b y-combinator"),
        ("y-combinator-square", " &#xf1d4 y-combinator-square"),
        ("yahoo", " &#xf19e yahoo"),
        ("yc", " &#xf23b yc"),
        ("yc-square", " &#xf1d4 yc-square"),
        ("yelp", " &#xf1e9 yelp"),
        ("yen", " &#xf157 yen"),
        ("yoast", " &#xf2b1 yoast"),
        ("youtube", " &#xf167 youtube"),
        ("youtube-play", " &#xf16a youtube-play"),
        ("youtube-square", " &#xf166 youtube-square"),

    ]

    topic_icon = forms.CharField(
        widget=forms.Select(choices=TOPIC_CHOICES))


    if use_pagedown:
        content_raw = forms.CharField(
            label=_('Content'), widget=PagedownWidget())


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(TopicForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))


    class Meta:
        model = Topic
        fields = ['node_group', 'title', 'description', 'topic_icon']
        labels = {
            'node_group': ('NodeGroup'),
            'description': ('Description'),
            'title': ('Title'),

        }


    def save(self, commit=True):
        inst = super(TopicForm, self).save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst




        if use_pagedown:
            content_raw = forms.CharField(
                label=_('Content'), widget=PagedownWidget())

        def __init__(self, *args, **kwargs):
            self.user = kwargs.pop('user', None)
            super(TopicForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.add_input(Submit('submit', _('Submit')))

        class Meta:
            model = Topic
            fields = ['node_group', 'title', 'description', 'topic_icon']
            labels = {
                'node_group': _('NodeGroup'),
                'description': _('Description'),
                'title': _('Title'),
                'topic_icon': _('Topic Icon'),
            }

    def save(self, commit=True):
        inst = super(TopicForm, self).save(commit=False)
        inst.center_associated_with = self.user.Center_Code
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class TopicEditForm(ModelForm):
    if use_pagedown:
        content_raw = forms.CharField(
            label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        super(TopicEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Topic
        fields = ('description', 'topic_icon',)
        labels = {
            'description': _('Description'),
            'topic_icon': _('Topic Icon'),
        }


class AppendixForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.thread = kwargs.pop('thread', None)
        super(AppendixForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Appendix
        fields = ('content_raw',)
        labels = {
            'content_raw': _('Content'),
        }

    def save(self, commit=True):
        inst = super(AppendixForm, self).save(commit=False)
        inst.thread = self.thread
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class ForumAvatarForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ForumAvatarForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = ForumAvatar
        fields = ('image', 'use_gravatar')
        labels = {
            'image': _('Avatar Image'),
            'use_gravatar': _("Always Use Gravatar")
        }

    def save(self, commit=True):
        inst = super(ForumAvatarForm, self).save(commit=False)
        inst.user = self.user
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class ReplyForm(ModelForm):
    if use_pagedown:
        content_raw = forms.CharField(label='', widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.thread_id = kwargs.pop('thread_id', None)
        super(ReplyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Post
        fields = ('content_raw',)
        labels = {
            'content_raw': '',
        }

    def save(self, commit=True):
        inst = super(ReplyForm, self).save(commit=False)
        inst.user = self.user
        inst.thread_id = self.thread_id
        if commit:
            inst.save()
            self.save_m2m()
        return inst


class PostEditForm(ModelForm):
    if use_pagedown:
        content_raw = forms.CharField(
            label=_('Content'), widget=PagedownWidget())

    def __init__(self, *args, **kwargs):
        super(PostEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Post
        fields = ('content_raw',)
        labels = {
            'content_raw': _('Content'),
        }
