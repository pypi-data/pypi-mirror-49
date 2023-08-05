# -*- encoding: utf-8 -*-
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from bpp.views.api.clarivate import GetWoSAMRInformation
from bpp.views.api.pubmed import GetPubmedIDView
from bpp.views.api.strona_tom_nr_zeszytu import StronaTomNrZeszytuView
from bpp.views.api.uzupelnij_rok import ApiUzupelnijRokWydawnictwoZwarteView, ApiUzupelnijRokWydawnictwoCiagleView

from bpp.views.oai import OAIView
from bpp.views.api import RokHabilitacjiView, PunktacjaZrodlaView, UploadPunktacjaZrodlaView, OstatniaJednostkaIDyscyplinaView
from bpp.views.browse import UczelniaView, WydzialView, JednostkaView, \
    AutorView, ZrodlaView, ZrodloView, AutorzyView, BuildSearch, PracaView, \
    JednostkiView, \
    OldPracaView
from bpp.views.autocomplete import WidocznaJednostkaAutocomplete, \
    AutorZUczelniAutocopmlete, GlobalNavigationAutocomplete, \
    JednostkaAutocomplete, ZrodloAutocomplete, AutorAutocomplete, \
    ZapisanyJakoAutocomplete, Wydawnictwo_NadrzedneAutocomplete, \
    PodrzednaPublikacjaHabilitacyjnaAutocomplete, \
    AdminNavigationAutocomplete, KonferencjaAutocomplete, \
    Seria_WydawniczaAutocomplete, OrganPrzyznajacyNagrodyAutocomplete, \
    WydzialAutocomplete, PublicAutorAutocomplete, LataAutocomplete, PublicWydzialAutocomplete, \
    Dyscyplina_NaukowaAutocomplete, Zewnetrzna_Baza_DanychAutocomplete, PublicKonferencjaAutocomplete, \
    Dyscyplina_Naukowa_PrzypisanieAutocomplete
from bpp.views.raporty import RankingAutorow, \
    PobranieRaportu, PodgladRaportu, KasowanieRaportu, \
    RaportJednostek2012, RaportKronikaUczelni, RaportJednostek, \
    RankingAutorowFormularz, RaportDlaKomisjiCentralnejFormularz, RaportSelector, \
    RaportAutorow
from bpp.views.raporty.raport_autorow_2012 import RaportAutorow2012
from bpp import reports

reports # PyCharm, leave that import alone, it is IMPORTANT to import it
import bpp
from django.conf import settings

urlpatterns = [
    url(r'^api/rok-habilitacji/$', csrf_exempt(RokHabilitacjiView.as_view()),
        name='api_rok_habilitacji'),
    url(r'^api/punktacja-zrodla/(?P<zrodlo_id>[\d]+)/(?P<rok>[\d]+)/$',
        csrf_exempt(PunktacjaZrodlaView.as_view()),
        name='api_punktacja_zrodla'),
    url(r'^api/upload-punktacja-zrodla/(?P<zrodlo_id>[\d]+)/(?P<rok>[\d]+)/$',
        csrf_exempt(UploadPunktacjaZrodlaView.as_view()),
        name='api_upload_punktacja_zrodla'),
    url(r'^api/ostatnia-jednostka-i-dyscyplina/$',
        csrf_exempt(OstatniaJednostkaIDyscyplinaView.as_view()),
        name='api_ostatnia_jednostka_i_dyscyplina'),
    url(r'^api/pubmed-id/$',
        csrf_exempt(GetPubmedIDView.as_view()),
        name='api_pubmed_id'),
    url(r'^api/(?P<slug>[\w-]+)/wos-amr/$',
        csrf_exempt(GetWoSAMRInformation.as_view()),
        name='api_wos_amr'),
    url(r'^api/strona-tom-nr-zeszytu/$',
        csrf_exempt(StronaTomNrZeszytuView.as_view()),
        name='api_strona_tom_nr_zeszytu'),
    url(r'^api/uzupelnij_rok_wydawnictwo_zwarte/$',
        csrf_exempt(ApiUzupelnijRokWydawnictwoZwarteView.as_view()),
        name='api_uzupelnij_rok_wydawnictwo_zwarte'),
    url(r'^api/uzupelnij_rok_wydawnictwo_ciagle/$',
        csrf_exempt(ApiUzupelnijRokWydawnictwoCiagleView.as_view()),
        name='api_uzupelnij_rok_wydawnictwo_ciagle'),

    url(r'^oai/', OAIView.as_view(), name="oai"),

    url(r'^jednostka/(?P<slug>[\w-]+)/$', JednostkaView.as_view(),
        name='browse_jednostka'),
    url(r'^jednostki/$', JednostkiView.as_view(), name="browse_jednostki"),
    url(r'^jednostki/(?P<literka>.)/$', JednostkiView.as_view(),
        name="browse_jednostki_literka"),
    url(r'^wydzial/(?P<slug>[\w-]+)/$', WydzialView.as_view(),
        name='browse_wydzial'),
    url(r'^uczelnia/(?P<slug>[\w-]+)/$',
        UczelniaView.as_view(),
        name='browse_uczelnia'),
    url(r'^uczelnia/(?P<slug>[\w-]+)/(?P<article_slug>[\w-]+)/$',
        UczelniaView.as_view(),
        name='browse_artykul'),
    url(r'^autorzy/$', AutorzyView.as_view(), name='browse_autorzy'),
    url(r'^autorzy/(?P<literka>.)/$', AutorzyView.as_view(),
        name='browse_autorzy_literka'),
    url(r'^autor/(?P<slug>[\w-]+)/$', AutorView.as_view(), name='browse_autor'),
    url(r'^zrodla/$', ZrodlaView.as_view(), name='browse_zrodla'),
    url(r'^zrodla/(?P<literka>.)/$', ZrodlaView.as_view(),
        name='browse_zrodla_literka'),
    url(r'^zrodlo/(?P<slug>[\w-]+)/$', ZrodloView.as_view(),
        name='browse_zrodlo'),

    url(r'^(?P<model>[\w_]+)/(?P<pk>[\d]+)/$', OldPracaView.as_view(), name='browse_praca_old'),
    url(r'^rekord/(?P<model>[\w_]+),(?P<pk>[\d]+)/$', PracaView.as_view(),
        name='browse_praca'),
    # url(r'^rekord/(?P<content_type_id>[\d]+),(?P<object_id>[\d]+)/$', RekordToPracaView.as_view(),
    #     name='browse_rekord'),

    url(r'^build_search/$', BuildSearch.as_view(), name='browse_build_search'),

    url(r'^raporty/$', login_required(RaportSelector.as_view()), name='raporty'),
    url(r'^raporty/kronika_uczelni/$', login_required(RaportKronikaUczelni.as_view()), name='raport_kronika_uczelni'),
    url(r'^raporty/jednostek/$', RaportJednostek.as_view(), name='raport_jednostek_formularz'),
    url(r'^raporty/autorow/$', RaportAutorow.as_view(), name='raport_autorow_formularz'),
    url(r'^raporty/ranking-autorow/wybierz/$', RankingAutorowFormularz.as_view(), name='ranking_autorow_formularz'),
    url(r'^raporty/dla-komisji-centralnej/$', login_required(RaportDlaKomisjiCentralnejFormularz.as_view()), name='raport_dla_komisji_centralnej'),


    url(r'^raporty/pobranie/(?P<uid>[\w-]+)/$',
        login_required(PobranieRaportu.as_view()), name='pobranie-raportu'),
    url(r'^raporty/podglad/(?P<uid>[\w-]+)/skasuj/$',
        login_required(KasowanieRaportu.as_view()), name='kasowanie-raportu'),
    url(r'^raporty/podglad/(?P<uid>[\w-]+)/$',
        login_required(PodgladRaportu.as_view()), name='podglad-raportu'),

    url(r'^raporty/ranking-autorow/(?P<od_roku>\d+)/(?P<do_roku>\d+)/$',
        RankingAutorow.as_view(), name='ranking-autorow'),

    url(
        r'^raporty/raport-jednostek-2012/(?P<pk>\d+)/(?P<rok_min>\d+)-(?P<rok_max>\d+)/$',
        RaportJednostek2012.as_view(),
        name='raport-jednostek-rok-min-max'),
    url(r'^raporty/raport-jednostek-2012/(?P<pk>\d+)/(?P<rok_min>\d+)/$',
        RaportJednostek2012.as_view(), name='raport-jednostek'),

    url(
        r'^raporty/raport-autorow-2012/(?P<pk>\d+)/(?P<rok_min>\d+)-(?P<rok_max>\d+)/$',
        RaportAutorow2012.as_view(),
        name='raport-autorow-rok-min-max'),
    url(r'^raporty/raport-autorow-2012/(?P<pk>\d+)/(?P<rok_min>\d+)/$',
        RaportAutorow2012.as_view(), name='raport-autorow'),

    url(r'^$', bpp.views.root, name="root"),

    url(r'^update-multiseek-title/$', bpp.views.update_multiseek_title,
        name='update_multiseek_title'),

    url(
        r'^konferencja-autocomplete/$',
        KonferencjaAutocomplete.as_view(),
        name='konferencja-autocomplete',
    ),
    url(
        r'^public-konferencja-autocomplete/$',
        PublicKonferencjaAutocomplete.as_view(),
        name='public-konferencja-autocomplete',
    ),
    url(
        r'^wydzial-autocomplete/$',
        WydzialAutocomplete.as_view(),
        name='wydzial-autocomplete',
    ),
    url(
        r'^public-wydzial-autocomplete/$',
        PublicWydzialAutocomplete.as_view(),
        name='public-wydzial-autocomplete',
    ),
    url(
        r'^seria-wydawnicza-autocomplete/$',
        Seria_WydawniczaAutocomplete.as_view(),
        name='seria-wydawnicza-autocomplete',
    ),
    url(
        r'^organ-przyznajacy-nagrody-autocomplete/$',
        OrganPrzyznajacyNagrodyAutocomplete.as_view(),
        name='organ-przyznajacy-nagrody-autocomplete',
    ),
    url(
        r'^jednostka-widoczna-autocomplete/$',
        WidocznaJednostkaAutocomplete.as_view(),
        name='jednostka-widoczna-autocomplete',
    ),

    url(
        r'^jednostka-autocomplete/$',
        JednostkaAutocomplete.as_view(),
        name='jednostka-autocomplete',
    ),

    url(
        r'^zewnetrzna-baza-danych-autocomplete/$',
        Zewnetrzna_Baza_DanychAutocomplete.as_view(),
        name='zewnetrzna-baza-danych-autocomplete',
    ),


    url(
        r'^dyscyplina-autocomplete/$',
        Dyscyplina_NaukowaAutocomplete.as_view(),
        name='dyscyplina-autocomplete',
    ),

    url(
        r'^zrodlo-autocomplete/$',
        ZrodloAutocomplete.as_view(),
        name='zrodlo-autocomplete',
    ),

    url(
        r'^autor-z-uczelni-autocomplete/$',
        AutorZUczelniAutocopmlete.as_view(),
        name='autor-z-uczelni-autocomplete',
    ),
    url(
        r'^autor-autocomplete/$',
        AutorAutocomplete.as_view(),
        name='autor-autocomplete',
    ),
    url(
        r'^public-autor-autocomplete/$',
        PublicAutorAutocomplete.as_view(),
        name='public-autor-autocomplete',
    ),
    url(
        r'^lata-autocomplete/$',
        LataAutocomplete.as_view(),
        name='lata-autocomplete',
    ),

    url(
        r'^navigation-autocomplete/$',
        GlobalNavigationAutocomplete.as_view(),
        name='navigation-autocomplete'
    ),

    url(
        r'^admin-navigation-autocomplete/$',
        AdminNavigationAutocomplete.as_view(),
        name='admin-navigation-autocomplete'
    ),

    url(
        r'^zapisany-jako-autocomplete/$',
        ZapisanyJakoAutocomplete.as_view(),
        name='zapisany-jako-autocomplete'
    ),

    url(
        r'^wydawnictwo-nadrzedne-autocomplete/$',
        Wydawnictwo_NadrzedneAutocomplete.as_view(),
        name='wydawnictwo-nadrzedne-autocomplete'
    ),

    url(
        r'^podrzedna-publikacja-habilitacyjna-autocomplete/$',
        PodrzednaPublikacjaHabilitacyjnaAutocomplete.as_view(),
        name='podrzedna-publikacja-habilitacyjna-autocomplete'
    ),

    url(
        r'^dyscyplina-naukowa-przypisanie-autocomplete/$',
        Dyscyplina_Naukowa_PrzypisanieAutocomplete.as_view(),
        name='dyscyplina-naukowa-przypisanie-autocomplete'
    )


]
from bpp import reports
