import json

class _AppAnalysisConstants:

    _PERMISSION_SIGNATURE = [
        'android.permission.BIND_ACCESSIBILITY_SERVICE',
        'android.permission.BIND_AUTOFILL_SERVICE',
        'android.permission.BIND_CARRIER_SERVICES',
        'android.permission.BIND_CHOOSER_TARGET_SERVICE',
        'android.permission.BIND_CONDITION_PROVIDER_SERVICE',
        'android.permission.BIND_DEVICE_ADMIN',
        'android.permission.BIND_DREAM_SERVICE',
        'android.permission.BIND_INCALL_SERVICE',
        'android.permission.BIND_INPUT_METHOD',
        'android.permission.BIND_MIDI_DEVICE_SERVICE',
        'android.permission.BIND_NFC_SERVICE',
        'android.permission.BIND_NOTIFICATION_LISTENER_SERVICE',
        'android.permission.BIND_PRINT_SERVICE',
        'android.permission.BIND_SCREENING_SERVICE',
        'android.permission.BIND_TELECOM_CONNECTION_SERVICE',
        'android.permission.BIND_TEXT_SERVICE',
        'android.permission.BIND_TV_INPUT',
        'android.permission.BIND_VISUAL_VOICEMAIL_SERVICE',
        'android.permission.BIND_VOICE_INTERACTION',
        'android.permission.BIND_VPN_SERVICE',
        'android.permission.BIND_VR_LISTENER_SERVICE',
        'android.permission.BIND_WALLPAPER',
        'android.permission.CLEAR_APP_CACHE',
        'android.permission.MANAGE_DOCUMENTS',
        'android.permission.READ_VOICEMAIL',
        'android.permission.REQUEST_INSTALL_PACKAGES',
        'android.permission.SYSTEM_ALERT_WINDOW',
        'android.permission.WRITE_SETTINGS',
        'android.permission.WRITE_VOICEMAIL'
    ]

    _PERMISSION_DANGERIOUS = [
        'android.permission.READ_CALENDAR',
        'android.permission.WRITE_CALENDAR',
        'android.permission.CAMERA',
        'android.permission.READ_CONTACTS',
        'android.permission.WRITE_CONTACTS',
        'android.permission.GET_ACCOUNTS',
        'android.permission.ACCESS_FINE_LOCATION',
        'android.permission.ACCESS_COARSE_LOCATION',
        'android.permission.RECORD_AUDIO',
        'android.permission.READ_PHONE_STATE',
        'android.permission.READ_PHONE_NUMBERS',
        'android.permission.CALL_PHONE',
        'android.permission.ANSWER_PHONE_CALLS',
        'android.permission.READ_CALL_LOG',
        'android.permission.WRITE_CALL_LOG',
        'android.permission.ADD_VOICEMAIL',
        'android.permission.USE_SIP',
        'android.permission.PROCESS_OUTGOING_CALLS',
        'android.permission.BODY_SENSORS',
        'android.permission.SEND_SMS',
        'android.permission.RECEIVE_SMS',
        'android.permission.READ_SMS',
        'android.permission.RECEIVE_WAP_PUSH',
        'android.permission.RECEIVE_MMS',
        'android.permission.READ_EXTERNAL_STORAGE',
        'android.permission.WRITE_EXTERNAL_STORAGE'
    ]

    _ANDROID_VERSIONS = [
        {'name': 'None', 'version': '10.1', 'api': '30'},
        {'name': 'popcorn', 'version': '9.1', 'api': '29'},
        {'name': 'popcorn', 'version': '9.0', 'api': '28'},
        {'name': 'oreo', 'version': '8.1', 'api': '27'},
        {'name': 'oreo', 'version': '8.0', 'api': '26'},
        {'name': 'nogat', 'version': '7.1.2', 'api': '25'},
        {'name': 'nogat', 'version': '7.1.1', 'api': '25'},
        {'name': 'nogat', 'version': '7.1', 'api': '25'},
        {'name': 'nogat', 'version': '7.0', 'api': '24'},
        {'name': 'marshmellow', 'version': '6.0.1', 'api': '23'},
        {'name': 'marshmellow', 'version': '6.0', 'api': '23'},
        {'name': 'lollipop', 'version': '5.1.1', 'api': '22'},
        {'name': 'lollipop', 'version': '5.1', 'api': '22'},
        {'name': 'lollipop', 'version': '5.0.2', 'api': '21'},
        {'name': 'lollipop', 'version': '5.0.1', 'api': '21'},
        {'name': 'lollipop', 'version': '5.0', 'api': '21'},
        {'name': 'kitkat', 'version': '4.4.4', 'api': '19'},
        {'name': 'kitkat', 'version': '4.4.3', 'api': '19'},
        {'name': 'kitkat', 'version': '4.4.2', 'api': '19'},
        {'name': 'kitkat', 'version': '4.4.1', 'api': '19'},
        {'name': 'kitkat', 'version': '4.4', 'api': '19'},
        {'name': 'jellybean', 'version': '4.3', 'api': '18'},
        {'name': 'jellybean', 'version': '4.2.2', 'api': '17'},
        {'name': 'jellybean', 'version': '4.2.1', 'api': '17'},
        {'name': 'jellybean', 'version': '4.2', 'api': '17'},
        {'name': 'jellybean', 'version': '4.1.2', 'api': '16'},
        {'name': 'jellybean', 'version': '4.2.1', 'api': '16'},
        {'name': 'jellybean', 'version': '4.1', 'api': '16'},
        {'name': 'icecreamsandwich', 'version': '4.0.4', 'api': '15'},
        {'name': 'icecreamsandwich', 'version': '4.0.3', 'api': '15'},
        {'name': 'icecreamsandwich', 'version': '4.0.2', 'api': '14'},
        {'name': 'icecreamsandwich', 'version': '4.0.1', 'api': '14'},
        {'name': 'icecreamsandwich', 'version': '4.0', 'api': '14'},
        {'name': 'honeycomb', 'version': '3.2.6', 'api': '13'},
        {'name': 'honeycomb', 'version': '3.2.4', 'api': '13'},
        {'name': 'honeycomb', 'version': '3.2.2', 'api': '13'},
        {'name': 'honeycomb', 'version': '3.2.1', 'api': '13'},
        {'name': 'honeycomb', 'version': '3.2', 'api': '13'},
        {'name': 'honeycomb', 'version': '3.1', 'api': '12'},
        {'name': 'honeycomb', 'version': '3.0', 'api': '11'},
        {'name': 'gingerbread', 'version': '2.3.7', 'api': '10'},
        {'name': 'gingerbread', 'version': '2.3.6', 'api': '10'},
        {'name': 'gingerbread', 'version': '2.3.5', 'api': '10'},
        {'name': 'gingerbread', 'version': '2.3.4', 'api': '10'},
        {'name': 'gingerbread', 'version': '2.3.3', 'api': '10'},
        {'name': 'gingerbread', 'version': '2.3', 'api': '9'},
        {'name': 'froyo', 'version': '2.2', 'api': '8'},
        {'name': 'eclair', 'version': '2.1', 'api': '7'},
        {'name': 'eclair', 'version': '2.0.1', 'api': '6'},
        {'name': 'eclair', 'version': '2.0', 'api': '5'},
        {'name': 'donut', 'version': '1.6', 'api': '4'},
        {'name': 'cupcake', 'version': '1.5', 'api': '3'},
        {'name': 'donut', 'version': '1.1', 'api': '2'},
        {'name': 'donut', 'version': '1.0', 'api': '1'},
        {'name': 'donut', 'version': '0.9', 'api': '0.1'},
    ]

    _RG_MANIFEST_SECRET = r'api|secret|appkey|\bkey\b|token'


class _Trackers:

	@classmethod
	def exodus_trackers(self, trackers):
		"""
		Use this method to override the build in _TRACKERS constant with 
		the response body from the exodus api. This is not recommended because 
		some of the detection regex's from exodus are not valid. Example 'CrowdTangle': '.' 
		The Exodus api url is https://reports.exodus-privacy.eu.org/api/trackers
		
		Parameters
		----------
		trackers : str
			the json response body from the exodus api.

		Examples
		--------
		>>> import requests
		>>> from glorifiedgrep.android.modules.constants import _Trackers
		>>> res = requests.get('https://reports.exodus-privacy.eu.org/api/trackers').text
		>>> _Trackers().exodus_trackers(res)
		"""
		data = json.loads(trackers)['trackers']
		self._TRACKERS = {data[k]['name']: data[k]['code_signature'] for k in data}

	_AD_NETWORKS = {
		'Admob': r'^import.+google.+ads.+',
		'Facebook': r'^import com.facebook.ads.*',
		'Unity Ads': r'^import com.unity3d.services.*',
		'AppLovin': r'^import com.applovin.sdk.*',
		'MoPub': r'^import com.mopub.*',
		'Appsflyer': r'^import com.appsflyer.*',
		'Vungle': r'^import com.vungle.warren.',
		'AdColony': r'^import com.adcolony.sdk',
		'Chartboost': r'^import com.chartboost.sdk.*',
		'Ironsource': r'^import com.supersonic.mediationsdk.sdk',
		'InMobi': r'^import com.inmobi.*',
		'Tapjob': r'^import com.tapjoy.*',
		'Adjust': r'^import com.adjust.sdk.*',
		'Amazon Mobile Ads': r'^import com.amazon.device.ads.*',
		'Mellinal Media': r'^import com.millennialmedia.*',
		'Mobvista': r'^import com.mobvista.sdk.*',
		'DU': r'^import com.duapps.ad.*',
		'Startapp': r'^import com.startapp.*',
		'HeyZap': r'^import com.heyzap.sdk.*',
		'Smaato': r'^import com.smaato.*',
		'AppNext': r'^import com.appnext.*',
		'Ogury': r'^import io.presage.*',
		'HyperMX': r'^import com.hyprmx.android.sdk.*',
		'Fyber': r'^import com.fyber.*',
		'MobileAppTracking': r'^import com.tune.*',
		'Cheetah Mobile Ads': r'^import com.cmcm.ads.*',
		'AerServ': r'^import com.aerserv.sdk.*',
		'Kochava': r'^import com.kochava.*',
		'Appodeal': r'^import com.appodeal.ads.*',
		'LeadBolt': r'^import com.apptracker.android.*',
		'Yume RhythmOne': r'^com.rhythmone.ad.*',
		'Bee7': r'^import com.bee7.sdk.*',
		'Avacarrot Glispa': r'^import com.avocarrot.*',
		'Mdotm Crosschannel': r'^import com.mdotm.android.*',
		'Appbrain': r'^import com.appbrain.*',
		'Receptiv': r'^import com.tapdaq.sdk.*',
		'Supersonic': r'^import com.supersonic.mediationsdk.sdk.*',
		'Display.io': r'^import io.display.*',
		'Tenjin': r'^import com.tenjin.android.*',
		'Tapdaq': r'^import com.tapdaq.sdk.*',
		'PubNative': r'^import net.pubnative.player.*',
		'Smart AdServer': r'^import com.smartadserver.android.library.*',
		'AppNexus': r'^import com.appnexus.opensdk.*',
		'Daum': r'^import net.daum.*',
		'Taboola': r'^import com.taboola.android.*',
		'TNK': r'^import com.tnkfactory.ad.*',
		'Nielsen': r'^import com.nielsen.app.sdk.*',
		'Pollfish': r'^import com.pollfish.*',
		'Nend': r'^import net.nend.android.*',
		'Revmob': r'^import com.revmob.*',
		'Adbubbiz': r'^import com.purplebrain.adbuddiz.*',
		'Upsight': r'^import com.upsight.*',
		'Adlib': r'^import com.mocoplex.adlib.*',
		'Youappi': r'^import com.youappi.sdk.*',
		'Freewheel Akamai': r'^import com.akamai.freewheel.*|^import com.akamai.ads.*',
		'Admarvel': r'^import com.admarvel.android.*',
		'Kiip': r'^import me.kiip.sdk.*',
		'Tappx': r'^com.tappx.sdk.*',
		'adPOPcorn': r'^import com.igaworks.adpopcorn.*',
		'MobFox': r'^import com.adsdk.sdk.*',
		'OpenX': r'^import com.openx.*',
		'NativeX': r'^import com.nativex.*',
		'Sponsorpay': r'^import com.sponsorpay.*',
		'Airpush': r'^import com.airpush.*',
		'Outbrain': r'import com.outbrain.*',
		'Tapcore': r'^import com.tapcore.*',
		'Calldorado': r'^import com.calldorado.*',
		'Noquosh': r'^import com.noqoush.*',
		'GetJar': r'^import com.getjar.sdk.*',
		'Verve': r'^import com.vervewireless.*',
		'Metaps': r'^import net.metaps.sdk.*',
		'Adwhirl': r'^import com.adwhirl.*',
		'Adstir': r'^import com.ad_stir.*',
		'MyTarget': r'^import com.my.target.*',
		'Adlantis': r'^import jp.Adlantis,*',
		'Appdriver': r'^import net.adways.appdriver.sdk.*',
		'Appia': r'^import com.appia.sdk.*',
		'Conversant': r'^import com.greystripe.*',
		'Jumptap': r'^import com.jumptap.*',
		'Amoad': r'^import com.amoad.*',
		'Vpon': r'^import com.vpadn.ads.*',
		'Wiyun': r'^import com.wiyun.*',
		'Mediba': r'^import mediba.ad.sdk.*',
		'Mobclix': r'^import com.mobclix.android.sdk.*',
		'Ampiri': r'^import com.ampiri.sdk.*',
		'Swelen': r'^import com.swelen.ads.*',
		'Madhouse': r'^import com.madhouse.android.*',
		'Cauly': r'^import com.fsn.cauly.*',
		'Silvermob': r'^import com.silvermob.sdk.*',
		'adad': r'^import ir.adad.*',
		'Nexage': r'^import ^org.nexage.sourceki.*',
		'Tapsense': r'^import com.tapsense.android.publisher.*',
		'Mobeleader': r'^import com.mobeleader.sps.*',
		'Lifstreet': r'^import com.lifestreet.android.*',
		'Pocket Change': r'^import com.pocketchange.*',
		'Domob': r'^import cn.domob.android.*',
		'Komli': r'^import com.komlimobile.sdk.*',
		'Burstly': r'^import com.burstly.*',
		'Mobeleader': r'^import com.mobeleader.sps.*',
		'Phunware': r'^import com.phunware.*',
		'Vdopia': r'^import com.vdopia.ads.*',
		'Madvertise': r'^import de.madvertise.*',
		'Youmi': r'^import net.youmi.*',
		'Mocean': r'^import com.MASTAdView.*',
		'Adsmogo': r'^import com.adsmogo.*',
		'Waps': r'^import cn.waps.*',
		'Senddroid': r'^import com.senddroid.*',
		'Axonix': r'^import com.axonix.*',
		'Adwo': r'^import com.sixth.adwoad.*',
		'Adiquity': r'^import com.adiquity.android.*',
		'Appsfire': r'^com.appsfire.*',
		'Moolah': r'^import com.moolah.*',
		'Mobwin': r'^import com.tencent.mobwin.*',
		'Airad': r'^import com.mt.airad.*',
		'lmmob': r'^import com.lmmob.ad.sdk.*',
		'mobisage': r'^import com.mobisage.android.*',
		'adwo': r'^import com.adwo.adsdk.*',
		'adchina': r'^import com.adchina.android.*',
		'winad': r'^import com.winad.android.*',
		'wooboo': r'^import com.wooboo.adlib_android.*',
		'baidu': r'^import com.baidu.mobads.*',
		'umengAd': r'^import com.umengAd.*',
		'fractalist': r'^import com.fractalist.*',
		'miidi': r'^import net.miidi.ad.*',
		'appmedia': r'^import cn.appmedia.ad.*',
		'suizong': r'^import com.suizong.mobplate.*',
		'inmobi': r'^import com.inmobi.androidsdk.*',
		'telead': r'^import com.telead.*',
		'aduu': r'^import cn.aduu.*',
		'momark': r'^import com.donson.momark.*',
		'doumob': r'^import com.doumob.*',
		'hidian': r'^import com.adzhidian.*',
		'huawei': r'^import com.huawei.hiad.*',
		'cavas': r'^import net.cavas.*',
		'unknown': r'^import com.yjfsdk.advertSdk.*',
		'unknown1': r'^import com.mobile.app.adlist.*',
		'juzi': r'^import com.juzi.main.*',
		'bypush': r'^import com.bypush.*',
		'jpush': r'^import cn.jpush.android.*',
		'zestadz': r'^import com.zestadz.*',
		'izp': r'^import com.izp.*',
		'lsense': r'^import com.l.adlib_android.*'
	}

	_TRACKERS = {
        # Updated 7/5/2019
        'ADLIB': 'com.mocoplex.adlib.',
		'ATInternet': 'com.atinternet.',
		'AccountKit': 'com.facebook.accountkit',
		'Ad4Screen': 'com.ad4screen.sdk',
		'AdColony': 'com.adcolony',
		'AdFit (Daum)': 'com.kakao.adfit.ads.',
		'Add Apt Tr': 'com.intentsoftware.addapptr.',
		'Adform': 'com.adform.sdk.',
		'Adfurikun': 'jp.tjkapp.adfurikunsdk.',
		'Adincube': 'com.adincube.sdk.',
		'Adjust': 'com.adjust.sdk.',
		'Adot': 'com.adotmob',
		'AdsWizz': '.adswizz.',
		'AerServ': 'com.aerserv.sdk.',
		'Alphonso': 'tv.alphonso.service',
		'Amazon Advertisement': 'com.amazon.device.ads',
		'Amazon Analytics': 'com.amazon.insights|com.amazonaws.mobileconnectors.pinpoint.analytics.',
		'Amazon Mobile Associates': 'com.amazon.device.associates',
		'Amplitude': 'com.amplitude.',
		'AppAnalytics': 'io.appanalytics.sdk',
		'AppBrain': 'com.appbrain.',
		'AppLovin': 'com.applovin',
		'AppMetrica': 'com.yandex.metrica.',
		'AppMonet': 'com.monet.',
		'AppNexus': 'com.appnexus.opensdk.',
		'AppSee': 'com.appsee.',
		'Appdynamics': 'com.appdynamics.',
		'Applause': 'com.applause.android.',
		'Appnext': 'com.appnext.',
		'Appodeal': 'com.appodeal.ads.',
		'AppsFlyer': 'com.appsflyer.',
		'Apptentive': 'com.apptentive.',
		'Apptimize': 'com.apptimize.',
		'Apteligent by VMWare (formerly Crittercism)': 'com.crittercism.app.Crittercism',
		'Areametrics': 'com.areametrics.areametricssdk|com.areametrics.nosdkandroid',
		'Auditude': 'com.auditude.ads',
		'Backelite': 'com.backelite.android.|com.backelite.bkdroid.',
		'Baidu APPX': 'com.baidu.appx',
		'Baidu Location': 'com.baidu.location',
		'Baidu Map': 'com.baidu.mapapi',
		'Baidu Maps': 'com.baidu.BaiduMap',
		'Baidu Mobile Ads': 'com.baidu.mobads',
		'Baidu Mobile Stat': 'com.baidu.mobstat',
		'Baidu Navigation': 'com.baidu.navi',
		'Batch': 'com.batch.android.',
		'BlueConic': 'com.blueconic',
		'BlueKai (acquired by Oracle)': 'com.bluekai.sdk.',
		'Branch': 'io.branch.',
		'Braze (formerly Appboy)': 'com.appboy',
		'Brightcove': 'com.brightcove',
		'Bugly': 'com.tencent.bugly.',
		'Bugsnag': 'com.bugsnag.',
		'Carnival': 'com.carnival.sdk|com.carnivalmobile',
		'ChartBoost': 'com.chartboost.sdk.',
		'Cheetah Ads': 'com.cmcm.',
		'CleverTap': 'com.clevertap.',
		'Cloudmobi': 'com.cloudtech.',
		'Colocator': 'net.crowdconnected.androidcolocator',
		'ComScore': 'com.comscore.',
		'Conviva': 'com.conviva.',
		'Countly': 'ly.count.android.',
		'Criteo': 'com.criteo.',
		# 'CrowdTangle': '.',
		'Cuebiq': 'com.cuebiq.cuebiqsdk.model.Collector|com.cuebiq.cuebiqsdk.receiver.CoverageReceiver',
		'DOV-E': 'com.dv.',
		'Demdex': 'com.adobe.mobile.Analytics',
		'Display': 'io.display.',
		'Duapps': 'com.duapps.',
		'Dynamic Yield': 'com.dynamicyield.',
		'Dynatrace': 'com.dynatrace.android.app.',
		'Ensighten': 'com.ensighten.',
		'Estimote': 'com.estimote.',
		'Eulerian': 'com.eulerian.android.sdk',
		'ExactTarget': 'com.exacttarget.',
		'Facebook Ads': 'com.facebook.ads',
		'Facebook Analytics': 'com.facebook.appevents',
		'Facebook Audience': 'com.facebook.audiencenetwork',
		'Facebook Login': 'com.facebook.login',
		'Facebook Notifications': 'com.facebook.notifications',
		'Facebook Places': 'com.facebook.places',
		'Facebook Share': 'com.facebook.share',
		'FidZup': 'com.fidzup.',
		'Fiksu': 'com.fiksu.asotracking',
		'Flurry': 'com.flurry.',
		'Foresee': 'com.foresee.sdk.ForeSee',
		'Fyber': 'com.fyber.',
		'Fyber SponsorPay': 'com.sponsorpay',
		'GameAnalytics': 'com.gameanalytics.sdk',
		'Gigya': 'com.gigya.',
		'Gimbal': 'com.gimbal.android',
		'Glispa Connect (Formerly Avocarrot)': 'com.avocarrot.sdk',
		'Google Ads': 'com.google.android.gms.ads.mediation.',
		'Google Analytics': 'com.google.android.apps.analytics.|com.google.android.gms.analytics.',
		'Google CrashLytics': 'io.fabric.|com.crashlytics.',
		'Google DoubleClick': 'com.google.android.gms.ads.doubleclick',
		'Google Firebase Analytics': 'com.google.firebase.analytics.|com.google.android.gms.measurement.',
		'Google Tag Manager': 'com.google.tagmanager',
		'HelpShift': 'com.helpshift',
		'Heyzap (bought by Fyber)': 'com.heyzap.sdk.ads.',
		'HockeyApp': 'net.hockeyapp.',
		'Houndify': 'com.hound',
		'HyperTrack': 'com.hypertrack|com.hypertracklive.|io.hypertrack',
		'HyprMX': 'com.hyprmx.android.sdk.',
		'INFOnline': 'de.infonline.',
		'Inmarket': 'com.inmarket',
		'Inmobi': 'com.inmobi',
		'Inrix': 'com.inrix.sdk',
		'Instabug': 'com.instabug.library.tracking|com.instabug.bug',
		'Instreamatic': 'com.instreamatic',
		'JW Player': 'com.longtailvideo.jwplayer.',
		'Kochava': 'com.kochava.base.Tracker|com.kochava.android.tracker.',
		'Kontakt': 'com.kontakt.sdk.android.',
		'Krux': 'com.krux.androidsdk',
		'LeanPlum': 'com.leanplum.',
		'Ligatus': '.LigatusManager|.LigatusViewClient|com.ligatus.android.adframework',
		'Lisnr': 'com.lisnr.',
		'Localytics': 'com.localytics.android.',
		'Locuslabs': 'com.locuslabs.sdk',
		'Loggly': 'com.github.tony19.timber.loggly|com.github.tony19.loggly|com.visiware.sync2ad.logger.loggly.',
		'MAdvertise': 'com.mngads.sdk|com.mngads.views|com.mngads.',
		'MParticle': 'com.mparticle',
		'Mapbox': 'com.mapbox.mapboxsdk.',
		'Matomo (Piwik)': 'org.piwik|org.piwik.mobile|org.matomo',
		'Millennial Media': 'com.millennialmedia.',
		'Mintegral': 'com.mintegral.',
		'MixPanel': 'com.mixpanel.',
		'Moat': 'com.moat.analytics.mobile.',
		'MobFox': 'com.mobfox.',
		'Mobile Engagement': 'com.ubikod.capptain.|com.microsoft.azure.engagement.',
		'Mobvista': 'com.mobvista.',
		'Moodmedia': 'com.moodmedia',
		'NativeX': 'com.nativex',
		'New Relic': 'com.newrelic.agent.',
		'Nexage': 'com.nexage.android.|org.nexage.',
		'Ogury Presage': 'io.presage.',
		'Omniture': 'com.omniture.|com.adobe.adms.measurement.',
		'OneSignal': 'com.onesignal.',
		'Ooyala': 'com.ooyala',
		'OpenX': 'com.openx.view.plugplay|com.openx.android_sdk_openx',
		'Optimizely': 'com.optimizely.',
		'OtherLevels': 'com.otherlevels.',
		'OutBrain': 'com.outbrain.',
		'Persona.ly': 'ly.persona.sdk',
		'Pilgrim': 'com.foursquare.pilgrim|com.foursquare.pilgrimsdk.android',
		'Placed': 'com.placed.client',
		'PubNative': 'net.pubnative',
		'Pushwoosh': 'com.pushwoosh',
		'Quantcast': 'com.quantcast.measurement.service.',
		'Radius Networks': 'com.radiusnetworks',
		'Retency': 'com.retency.sdk.android',
		'Rubicon Project': 'com.rfm.sdk',
		'S4M': 'com.sam4mobile.',
		'Safe Graph': 'com.safegraph.|com.openlocate',
		'Scandit': 'com.scandit.',
		'Schibsted': '.schibsted.',
		'Segment': 'com.segment.analytics.',
		'Sense360': 'com.sense360.android.quinoa.lib.Sense360',
		'Sensoro': 'com.sensoro.beacon.kit.|com.sensoro.cloud',
		'ShallWeAD': 'com.jm.co.shallwead.sdk.|com.co.shallwead.sdk.',
		'Shopkick': 'com.shopkick.sdk.api.|com.shopkick.fetchers.',
		'Signal360': 'com.signal360.sdk.core.|com.sonicnotify.sdk.core.|com.rnsignal360',
		'SilverPush': 'com.silverpush.|com.silverpush.location|com.silverpush.sdk.android.SPService',
		'Singlespot': 'com.sptproximitykit.',
		'Sizmek': '.sizmek.',
		'Smaato': 'com.smaato.soma.',
		'Smart': 'com.smartadserver.',
		'Snowplow': 'com.snowplowanalytics.',
		'Soomla': 'com.soomla.',
		'Startapp': 'com.startapp.android.publish',
		'Supersonic Ads': 'com.supersonic.adapters.supersonicads|com.supersonicads.sdk',
		'Swrve': 'com.swrve.sdk',
		'Sync2Ad': 'com.visiware.sync2ad.dmp.',
		'Taboola': 'com.taboola.',
		'Tag Commander': 'com.tagcommander.',
		'Tapjoy': 'com.tapjoy.',
		'Taplytics': 'com.taplytics.sdk',
		'Tealium': '.tealium.',
		'Teemo': 'com.databerries.|com.geolocstation.',
		'TeleQuid': 'com.telequid.',
		'Tencent MTA': 'com.tencent.mta',
		'Tencent Map LBS': 'com.tencent.lbs',
		'Tencent MobWin': 'com.tencent.mobwin',
		'Tencent Stats': 'com.tencent.stat',
		'Tencent Weiyun': 'com.tencent.weiyun',
		'Tinder Analytics': 'com.tinder.analytics|com.tinder.ads',
		'Tune': 'com.tune|com.mobileapptracker',
		'Twitter MoPub': 'com.mopub.mobileads.',
		'Uber Analytics': 'com.ubercab.analytics.|com.ubercab.library.metrics.analytics.|com.ubercab.client.core.analytics.',
		'Umeng Analytics': 'com.umeng.analytics',
		'Umeng Feedback': 'com.umeng.fb',
		'Unity3d Ads': 'com.unity3d.services|com.unity3d.ads',
		'Urbanairship': 'com.urbanairship',
		'Vectaury': 'io.vectaury.',
		'Vungle': 'com.vungle.publisher.',
		'WeChat Location': 'com.tencent.map.geolocation|com.tencent.mm.plugin.location.|com.tencent.mm.plugin.location_soso.|com.tencent.mm.plugin.location_google',
		'Weborama': 'com.weborama.',
		'Webtrends': 'com.webtrends.mobile.analytics.|com.webtrends.mobile.android',
		'Widespace': 'com.widespace.',
		# 'Xiti': 'NC',
		'Yandex Ad': 'com.yandex.mobile.ads',
		'Yinzcam Sobek': 'com.yinzcam.sobek',
		'deltaDNA': 'com.deltadna',
		'ironSource': 'com.ironsource.',
		'myTarget': 'com.my.target.',
		'myTracker': 'com.my.tracker.'
    }


class _GrepConstants:

    _IGNORE_IMPORTS = r'^([^import].+)'

    _RG_INTENT_EXTRAS = {
        'getExtras': r"getExtras\(\s*[0-9A-Za-z_\"'.]+",
        'getStringExtra': r"getStringExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getIntExtra': r"getIntExtra\s*[0-9A-Za-z_\"'.]+",
        'getIntArrayExtra': r"getIntArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getFloatExtra': r"getFloatExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getFloatArrayExtra': r"getFloatArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getDoubleExtra': r"getDoubleExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getDoubleArrayExtra': r"getDoubleArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getCharExtra': r"getCharExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getCharArrayExtra': r"getCharArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getByteExtra': r"getByteExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getByteArrayExtra': r"getByteArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getBundleExtra': r"getBundleExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getBooleanExtra': r"getBooleanExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getBooleanArrayExtra': r"getBooleanArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getCharSequenceArrayExtra': r"getCharSequenceArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getCharSequenceArrayListExtra': r"getCharSequenceArrayListExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getCharSequenceExtra': r"getCharSequenceExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getInterArrayListExtra': r"getInterArrayListExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getLongArrayExtra': r"getLongArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getLongExtra': r"getLongExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getParcelableArrayExtra': r"getParcelableArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getParcelableArrayListExtra': r"getParcelableArrayListExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getParcelableExtra': r"getParcelableExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getSeriablizableExtra': r"getSeriablizableExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getShortArrayExtra': r"getShortArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getShortExtra': r"getShortExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getStringArrayExtra': r"getStringArrayExtra\(\s*[0-9A-Za-z_\"'.]+",
        'getStringArrayListExtra': r"getStringArrayListExtra\(\s*[0-9A-Za-z_\"'.]+"
    }
