using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class SoundManager : MonoBehaviour
{

    static SoundManager _instance;

    const float maxVolume_BGM = 1f;
    const float maxVolume_SFX = 1f;
    static float currentVolumeNormalized_BGM = 1f;
    static float currentVolumeNormalized_SFX = 1f;
    static bool isMuted = false;

    List<AudioSource> sfxSources;
    AudioSource bgmSource;


    public static SoundManager GetInstance()
    {
        if (!_instance)
        {
            GameObject soundManager = new GameObject("SoundManager");
            _instance = soundManager.AddComponent<SoundManager>();//??
            _instance.Initialize();
        }

        return _instance;
    }

    void Initialize()
    {
        //Add BGM sound Source
        bgmSource = gameObject.AddComponent<AudioSource>(); //??
        bgmSource.loop = true;
        bgmSource.playOnAwake = false;
        bgmSource.volume = GetBGMVolume();
        DontDestroyOnLoad(gameObject);
    }

    static float GetBGMVolume() //Get Background Music Volume
    {
        return isMuted ? 0f : maxVolume_BGM * currentVolumeNormalized_BGM;
    }

    static float GetSFXVolume() //Get Sound Effects Volume
    {
        return isMuted ? 0f : maxVolume_SFX * currentVolumeNormalized_SFX;
    }

    void FadeBGMOut (float fadeDuration)
    {
        SoundManager soundMan = GetInstance();
        float delay = 0f;
        float toVolume = 0f;

        if(soundMan.bgmSource.clip == null)
        {
            Debug.LogError("Error: Could no fade BGM out as the BGM AudioSource has no currently playing clip.");
        }

        StartCoroutine(FadeBGM(toVolume, delay, fadeDuration));
    }

    void FadeBGMIn (AudioClip bgmClip, float delay, float fadeDuration)
    {
        SoundManager soundMan = GetInstance();
        soundMan.bgmSource.clip = bgmClip;
        soundMan.bgmSource.Play();

        float toVolume = GetBGMVolume();

        StartCoroutine(FadeBGM(toVolume, delay, fadeDuration));
    }

    IEnumerator FadeBGM(float fadeToVolume, float delay, float duration)
    {
        yield return new WaitForSeconds(delay);

        SoundManager soundMan = GetInstance();
        float elapsed = 0f;
        while (duration > 0)
        {
        
            float t = (elapsed / duration);
            duration -= Time.deltaTime;
            float volume = Mathf.Lerp(0f, fadeToVolume * currentVolumeNormalized_BGM, t);
            soundMan.bgmSource.volume = volume;
            elapsed += Time.deltaTime;
            yield return 0;
        }
    }

    public static void PlayBGM(AudioClip bgmClip, bool fade, float fadeDuration)
    {
        SoundManager soundMan = GetInstance();

        if (fade)
        {
            if (soundMan.bgmSource.isPlaying)
            {
                //Fade out then in
                //soundMan.FadeBGMOut (fadeDuration / 2);
                soundMan.FadeBGMIn(bgmClip, fadeDuration, fadeDuration);

                //soundMan.StartCoroutine(soundMan.Countdown(soundMan, bgmClip, fade, fadeDuration));

            }
            else
            {
                //Just fade in
                float delay = 0f;
                soundMan.FadeBGMIn(bgmClip, delay, fadeDuration);
            }

        }
        else
        {
            //Play Immediately
            soundMan.bgmSource.volume = GetBGMVolume();
            soundMan.bgmSource.clip = bgmClip;
            soundMan.bgmSource.Play();
        }
    }
    IEnumerator Countdown(SoundManager soundMan, AudioClip bgmClip, bool fade, float fadeDuration)
    {
        yield return new WaitForSeconds(3);
        soundMan.FadeBGMIn(bgmClip, fadeDuration / 2, fadeDuration / 2);
    }

    public static void StopBGM(bool fade, float fadeDuration)
    {
        SoundManager soundMan = GetInstance();

        if (soundMan.bgmSource.isPlaying)
        {
            //Fade out then switch and fade in
            if (fade)
            {
                soundMan.FadeBGMOut(fadeDuration);
            }
            else
            {
                soundMan.bgmSource.Stop();
            }
        }
    }

    // ************************************ SFX Utilities ******************************************

    AudioSource GetSFXSource()
    {
        AudioSource sfxSource = gameObject.AddComponent<AudioSource>();
        sfxSource.loop = false;
        sfxSource.playOnAwake = false;
        sfxSource.volume = GetSFXVolume();

        if (sfxSources == null)
        {
            sfxSources = new List<AudioSource>();
        }

        sfxSources.Add(sfxSource);

        return sfxSource;
    }

    IEnumerator RemoveSFXSource(AudioSource sfxSource)
    {
        if (sfxSource.clip != null)
        {
            yield return new WaitForSeconds(sfxSource.clip.length);
            sfxSources.Remove(sfxSource);
            Destroy(sfxSource);
        }
    }

    IEnumerator RemoveSFXSourceFixedLength(AudioSource sfxSource, float length)
    {
        yield return new WaitForSeconds(length);
        sfxSources.Remove(sfxSource);
        Destroy(sfxSource);
    }

    public static void PlaySFX(AudioClip sfxClip)
    {
        SoundManager soundMan = GetInstance();
        AudioSource source = soundMan.GetSFXSource();
        source.volume = GetSFXVolume();
        source.clip = sfxClip;
        source.Play();

        soundMan.StartCoroutine(soundMan.RemoveSFXSource(source));
    }

    public static void PlaySFXRandomized(AudioClip sfxClip)
    {
        SoundManager soundMan = GetInstance();
        AudioSource source = soundMan.GetSFXSource();
        source.volume = GetSFXVolume();
        source.clip = sfxClip;
        source.pitch = Random.Range(0.85f, 1.2f);
        source.Play();

        soundMan.StartCoroutine(soundMan.RemoveSFXSource(source));
    }

    public static void PlaySFXFixedDuration(AudioClip sfxClip, float duration, float volumeMultplier = 1.0f)
    {
        SoundManager soundMan = GetInstance();
        AudioSource source = soundMan.GetSFXSource();
        source.volume = GetSFXVolume() * volumeMultplier;
        source.clip = sfxClip;
        source.loop = true;
        source.Play();

        soundMan.StartCoroutine(soundMan.RemoveSFXSource(source));
    }

    public static void DisableSoundImmediate()
    {
        SoundManager soundMan = GetInstance();
        soundMan.StopAllCoroutines();
        if (soundMan.sfxSources != null)
        {
            foreach (AudioSource source in soundMan.sfxSources)
            {
                source.volume = 0;
            }
        }
        soundMan.bgmSource.volume = 0f;
        isMuted = true;
    }

    public static void EnableSoundImmediate()
    {
        SoundManager soundMan = GetInstance();
        if(soundMan.sfxSources != null)
        {
            foreach (AudioSource source in soundMan.sfxSources)
            {
                source.volume = GetSFXVolume();
            }
        }
        soundMan.bgmSource.volume = GetBGMVolume();
        isMuted = false;
    }

    public static void SetGlobalVolume(float newVolume)
    {
        currentVolumeNormalized_BGM = newVolume;
        currentVolumeNormalized_SFX = newVolume;
    }

    public static void SetSFXVolume (float newVolume)
    {
        currentVolumeNormalized_SFX = newVolume;
    }



    public static void AdjustSoundImmediate()
    {
        SoundManager soundMan = GetInstance();
        if (soundMan.sfxSources != null)
        {
            foreach (AudioSource source in soundMan.sfxSources)
            {
                source.volume = GetSFXVolume();
            }
        }

        Debug.Log("BGM Volume: " + GetBGMVolume());
        soundMan.bgmSource.volume = GetBGMVolume();
        Debug.Log("BGM Volume is now: " + GetBGMVolume());
    }
}
