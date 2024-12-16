package com.droid.cryptor;

import android.os.Bundle;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import com.droid.cryptor.databinding.FragmentEncryptBinding;
import com.droid.cryptor.databinding.FragmentEncryptedBinding;

import java.security.InvalidAlgorithmParameterException;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;

import javax.crypto.BadPaddingException;
import javax.crypto.IllegalBlockSizeException;
import javax.crypto.NoSuchPaddingException;


public class EncryptedFragment extends Fragment {

    private FragmentEncryptedBinding binding;

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentEncryptedBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        assert getArguments() != null;
        AesLaboratory aes = new AesLaboratory(getArguments().getString("data"));


        try {
            binding.outputIV.setText(aes.getIV());
        } catch (Throwable e) {
            Log.e("EncryptedFragment", "onViewCreated: ", e);
        }

        try {
            binding.outputEncrypted.setText(aes.encrypt());
        } catch (Throwable e) {
            Log.e("EncryptedFragment", "onViewCreated: ", e);
        }



    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}