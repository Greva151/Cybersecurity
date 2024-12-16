package com.droid.cryptor;

import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;

import androidx.annotation.NonNull;
import androidx.fragment.app.Fragment;
import androidx.navigation.fragment.NavHostFragment;

import com.droid.cryptor.databinding.FragmentWelcomeBinding;

public class WelcomeFragment extends Fragment {

    private FragmentWelcomeBinding binding;

    @Override
    public View onCreateView(
            @NonNull LayoutInflater inflater, ViewGroup container,
            Bundle savedInstanceState
    ) {

        binding = FragmentWelcomeBinding.inflate(inflater, container, false);
        return binding.getRoot();

    }

    public void onViewCreated(@NonNull View view, Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        binding.decrypt.setOnClickListener(v ->
                NavHostFragment.findNavController(WelcomeFragment.this)
                        .navigate(R.id.action_FirstFragment_to_DecryptFragment)

        );

        binding.encrypt.setOnClickListener(v ->
                NavHostFragment.findNavController(WelcomeFragment.this)
                        .navigate(R.id.action_FirstFragment_to_EncryptFragment2)

        );
    }

    @Override
    public void onDestroyView() {
        super.onDestroyView();
        binding = null;
    }

}