package com.droid.cryptor;

import android.util.Base64;

import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Random;

import javax.crypto.BadPaddingException;
import javax.crypto.Cipher;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;

public class AesLaboratory {

    private static final String SUPER_SECRET_KEY = "YWYwYjAyYjkzNmRhZjU3Yg==";

    private final String data;
    private final byte[] IV;

    public static String generateRandomString(int length) {
        if (length <= 0) {
            throw new IllegalArgumentException("Length must be greater than 0");
        }

        String characterPool = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
        StringBuilder randomString = new StringBuilder(length);
        Random random = new Random();

        for (int i = 0; i < length; i++) {
            int randomIndex = random.nextInt(characterPool.length());
            randomString.append(characterPool.charAt(randomIndex));
        }

        return randomString.toString();
    }

    public AesLaboratory(String data) {
        this.data = data;
        this.IV = generateRandomString(16).getBytes();
    }

    public String getIV() {
        return Base64.encodeToString(IV, Base64.DEFAULT);
    }

    public String encrypt() throws InvalidAlgorithmParameterException, InvalidKeyException, NoSuchPaddingException, NoSuchAlgorithmException, IllegalBlockSizeException, BadPaddingException {
        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
        SecretKey secretKey = new SecretKeySpec(Base64.decode(SUPER_SECRET_KEY, Base64.DEFAULT), "AES");
        GCMParameterSpec gcmParameterSpec = new GCMParameterSpec(128, this.IV);

        cipher.init(Cipher.ENCRYPT_MODE, secretKey, gcmParameterSpec);
        byte[] encryptedData = cipher.doFinal(this.data.getBytes());

        return Base64.encodeToString(encryptedData, Base64.DEFAULT);

    }
}
